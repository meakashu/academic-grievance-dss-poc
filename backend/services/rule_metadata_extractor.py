"""
Rule Metadata Extractor Service
Parses DRL metadata blocks and exposes rule provenance information
"""
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RuleMetadataExtractor:
    """Service for extracting metadata from DRL rule files"""
    
    def __init__(self, rules_directory: str = None):
        """
        Initialize metadata extractor
        
        Args:
            rules_directory: Path to directory containing .drl files
        """
        if rules_directory is None:
            # Default to rules directory relative to backend
            backend_path = Path(__file__).parent.parent
            self.rules_directory = backend_path.parent / "rules"
        else:
            self.rules_directory = Path(rules_directory)
        
        self._metadata_cache = {}
        self._load_all_metadata()
    
    
    def _load_all_metadata(self):
        """Load metadata from all DRL files in rules directory"""
        if not self.rules_directory.exists():
            logger.warning(f"Rules directory not found: {self.rules_directory}")
            return
        
        drl_files = list(self.rules_directory.glob("*.drl"))
        logger.info(f"Found {len(drl_files)} DRL files in {self.rules_directory}")
        
        for drl_file in drl_files:
            try:
                file_metadata = self.parse_drl_metadata(str(drl_file))
                self._metadata_cache.update(file_metadata)
                logger.info(f"Loaded {len(file_metadata)} rules from {drl_file.name}")
            except Exception as e:
                logger.error(f"Error parsing {drl_file.name}: {e}")
    
    
    def parse_drl_metadata(self, drl_file_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse metadata from a DRL file
        
        Args:
            drl_file_path: Path to .drl file
            
        Returns:
            Dictionary mapping rule names to their metadata
        """
        metadata_dict = {}
        
        try:
            with open(drl_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract all rules with their metadata
            rule_pattern = r'rule\s+"([^"]+)".*?metadata\s*\{(.*?)\}.*?when(.*?)then(.*?)end'
            matches = re.finditer(rule_pattern, content, re.DOTALL)
            
            for match in matches:
                rule_name = match.group(1)
                metadata_block = match.group(2)
                when_clause = match.group(3)
                then_clause = match.group(4)
                
                # Parse metadata block
                metadata = self._parse_metadata_block(metadata_block)
                
                # Add rule structure info
                metadata['rule_name'] = rule_name
                metadata['when_clause'] = when_clause.strip()[:200] + "..." if len(when_clause.strip()) > 200 else when_clause.strip()
                metadata['then_clause'] = then_clause.strip()[:200] + "..." if len(then_clause.strip()) > 200 else then_clause.strip()
                metadata['source_file'] = os.path.basename(drl_file_path)
                
                metadata_dict[rule_name] = metadata
            
            # Also extract salience from rule declaration
            salience_pattern = r'rule\s+"([^"]+)".*?salience\s+(\d+)'
            salience_matches = re.finditer(salience_pattern, content, re.DOTALL)
            
            for match in salience_matches:
                rule_name = match.group(1)
                salience = int(match.group(2))
                if rule_name in metadata_dict:
                    metadata_dict[rule_name]['salience'] = salience
            
        except Exception as e:
            logger.error(f"Error parsing DRL file {drl_file_path}: {e}")
            raise
        
        return metadata_dict
    
    
    def _parse_metadata_block(self, metadata_block: str) -> Dict[str, Any]:
        """
        Parse individual metadata block
        
        Args:
            metadata_block: Metadata content between { }
            
        Returns:
            Dictionary of metadata key-value pairs
        """
        metadata = {}
        
        # Parse key: value pairs
        lines = metadata_block.strip().split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                # Remove trailing comma
                line = line.rstrip(',')
                
                # Split on first colon
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                
                metadata[key] = value
        
        return metadata
    
    
    def get_rule_metadata(self, rule_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific rule
        
        Args:
            rule_name: Name of the rule
            
        Returns:
            Metadata dictionary or None if not found
        """
        return self._metadata_cache.get(rule_name)
    
    
    def get_all_rules_metadata(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all rules
        
        Returns:
            List of metadata dictionaries
        """
        return list(self._metadata_cache.values())
    
    
    def get_rules_by_level(self, hierarchy_level: str) -> List[Dict[str, Any]]:
        """
        Get all rules at a specific hierarchy level
        
        Args:
            hierarchy_level: L1_National, L2_Accreditation, or L3_University
            
        Returns:
            List of rules at that level
        """
        return [
            metadata for metadata in self._metadata_cache.values()
            if metadata.get('level') == hierarchy_level
        ]
    
    
    def get_rules_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all rules in a specific category
        
        Args:
            category: Attendance, Examination, Fee, etc.
            
        Returns:
            List of rules in that category
        """
        return [
            metadata for metadata in self._metadata_cache.values()
            if metadata.get('category', '').lower() == category.lower()
        ]
    
    
    def get_rules_by_authority(self, authority: str) -> List[Dict[str, Any]]:
        """
        Get all rules from a specific authority
        
        Args:
            authority: UGC, NAAC, NBA, etc.
            
        Returns:
            List of rules from that authority
        """
        return [
            metadata for metadata in self._metadata_cache.values()
            if authority.lower() in metadata.get('authority', '').lower()
        ]
    
    
    def search_rules(self, query: str) -> List[Dict[str, Any]]:
        """
        Search rules by keyword
        
        Args:
            query: Search query
            
        Returns:
            List of matching rules
        """
        query_lower = query.lower()
        results = []
        
        for metadata in self._metadata_cache.values():
            # Search in rule name, description, authority, source
            searchable_text = ' '.join([
                metadata.get('rule_name', ''),
                metadata.get('description', ''),
                metadata.get('authority', ''),
                metadata.get('source', '')
            ]).lower()
            
            if query_lower in searchable_text:
                results.append(metadata)
        
        return results
    
    
    def get_hierarchy_summary(self) -> Dict[str, Any]:
        """
        Get summary of rule hierarchy
        
        Returns:
            Summary with counts by level
        """
        summary = {
            'total_rules': len(self._metadata_cache),
            'by_level': {},
            'by_category': {},
            'by_authority': {}
        }
        
        # Count by level
        for metadata in self._metadata_cache.values():
            level = metadata.get('level', 'Unknown')
            summary['by_level'][level] = summary['by_level'].get(level, 0) + 1
            
            category = metadata.get('category', 'Unknown')
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
            
            authority = metadata.get('authority', 'Unknown')
            summary['by_authority'][authority] = summary['by_authority'].get(authority, 0) + 1
        
        return summary


# Singleton instance
_metadata_extractor: Optional[RuleMetadataExtractor] = None


def get_rule_metadata_extractor() -> RuleMetadataExtractor:
    """Get or create rule metadata extractor instance"""
    global _metadata_extractor
    if _metadata_extractor is None:
        _metadata_extractor = RuleMetadataExtractor()
    return _metadata_extractor
