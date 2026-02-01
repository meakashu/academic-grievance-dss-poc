"""
Database service for PostgreSQL operations
Handles CRUD operations for grievances, decisions, and rule traces
"""
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import SimpleConnectionPool
from typing import Optional, List, Dict, Any
from uuid import UUID
import logging
from contextlib import contextmanager

from config import settings

logger = logging.getLogger(__name__)


class DatabaseService:
    """Service for database operations"""
    
    def __init__(self, min_conn: int = 1, max_conn: int = 10):
        """
        Initialize database connection pool
        
        Args:
            min_conn: Minimum number of connections
            max_conn: Maximum number of connections
        """
        try:
            self.pool = SimpleConnectionPool(
                min_conn,
                max_conn,
                host=settings.postgres_host,
                port=settings.postgres_port,
                database=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password
            )
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {str(e)}")
            raise
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = self.pool.getconn()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            self.pool.putconn(conn)
    
    # ==================== Grievance Operations ====================
    
    def create_grievance(self, student_id: str, grievance_type: str,
                        narrative: str, parameters: Dict[str, Any]) -> UUID:
        """
        Create a new grievance
        
        Args:
            student_id: Student identifier
            grievance_type: Type of grievance
            narrative: Student's narrative
            parameters: Structured parameters
            
        Returns:
            UUID of created grievance
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO grievances (student_id, grievance_type, narrative, parameters)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (student_id, grievance_type, narrative, Json(parameters)))
                
                grievance_id = cur.fetchone()[0]
                logger.info(f"Created grievance {grievance_id} for student {student_id}")
                return grievance_id
    
    def get_grievance(self, grievance_id: UUID) -> Optional[Dict[str, Any]]:
        """Get grievance by ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM grievances WHERE id = %s
                """, (str(grievance_id),))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def get_grievances_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        """Get all grievances for a student"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM grievances 
                    WHERE student_id = %s
                    ORDER BY submitted_at DESC
                """, (student_id,))
                
                return [dict(row) for row in cur.fetchall()]
    
    def update_grievance_status(self, grievance_id: UUID, status: str) -> bool:
        """Update grievance status"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE grievances 
                    SET status = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (status, str(grievance_id)))
                
                return cur.rowcount > 0
    
    # ==================== Decision Operations ====================
    
    def create_decision(self, grievance_id: UUID, outcome: str,
                       applicable_rule: str, regulatory_source: str,
                       hierarchy_level: str, salience: int, reason: str,
                       explanation: Optional[str] = None,
                       action_required: Optional[str] = None,
                       human_review_required: bool = False) -> UUID:
        """Create a new decision"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO decisions (
                        grievance_id, outcome, applicable_rule, regulatory_source,
                        hierarchy_level, salience, reason, explanation,
                        action_required, human_review_required
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    str(grievance_id), outcome, applicable_rule, regulatory_source,
                    hierarchy_level, salience, reason, explanation,
                    action_required, human_review_required
                ))
                
                decision_id = cur.fetchone()[0]
                logger.info(f"Created decision {decision_id} for grievance {grievance_id}")
                return decision_id
    
    def get_decision(self, decision_id: UUID) -> Optional[Dict[str, Any]]:
        """Get decision by ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM decisions WHERE id = %s
                """, (str(decision_id),))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def get_decision_by_grievance(self, grievance_id: UUID) -> Optional[Dict[str, Any]]:
        """Get decision for a grievance"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM decisions 
                    WHERE grievance_id = %s
                    ORDER BY decided_at DESC
                    LIMIT 1
                """, (str(grievance_id),))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    # ==================== Rule Trace Operations ====================
    
    def create_rule_trace(self, grievance_id: UUID, decision_id: Optional[UUID],
                         rules_evaluated: List[Dict[str, Any]],
                         conflicts_detected: List[Dict[str, Any]],
                         final_decision: Dict[str, Any],
                         processing_time_ms: int) -> UUID:
        """Create a new rule trace"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO rule_traces (
                        grievance_id, decision_id, rules_evaluated,
                        conflicts_detected, final_decision, processing_time_ms
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    str(grievance_id),
                    str(decision_id) if decision_id else None,
                    Json(rules_evaluated),
                    Json(conflicts_detected),
                    Json(final_decision),
                    processing_time_ms
                ))
                
                trace_id = cur.fetchone()[0]
                logger.info(f"Created rule trace {trace_id} for grievance {grievance_id}")
                return trace_id
    
    def get_rule_trace(self, trace_id: UUID) -> Optional[Dict[str, Any]]:
        """Get rule trace by ID"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM rule_traces WHERE id = %s
                """, (str(trace_id),))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    def get_rule_trace_by_grievance(self, grievance_id: UUID) -> Optional[Dict[str, Any]]:
        """Get rule trace for a grievance"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT * FROM rule_traces 
                    WHERE grievance_id = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (str(grievance_id),))
                
                result = cur.fetchone()
                return dict(result) if result else None
    
    # ==================== Fairness Operations ====================
    
    def find_similar_cases(self, grievance_type: str, parameters: Dict[str, Any],
                          limit: int = 10) -> List[Dict[str, Any]]:
        """
        Find similar historical cases for fairness comparison
        
        Args:
            grievance_type: Type of grievance
            parameters: Grievance parameters
            limit: Maximum number of cases to return
            
        Returns:
            List of similar cases with their decisions
        """
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Find cases with same type and similar parameters
                cur.execute("""
                    SELECT 
                        g.id as grievance_id,
                        g.student_id,
                        g.parameters,
                        d.outcome,
                        d.applicable_rule,
                        d.hierarchy_level,
                        d.decided_at
                    FROM grievances g
                    JOIN decisions d ON g.id = d.grievance_id
                    WHERE g.grievance_type = %s
                      AND g.status = 'RESOLVED'
                    ORDER BY g.submitted_at DESC
                    LIMIT %s
                """, (grievance_type, limit))
                
                return [dict(row) for row in cur.fetchall()]
    
    def create_fairness_check(self, grievance_id: UUID, decision_id: Optional[UUID],
                             similar_cases: List[Dict[str, Any]],
                             consistency_score: float,
                             anomaly_detected: bool,
                             demographic_parity: Optional[Dict[str, Any]] = None) -> UUID:
        """Create a fairness check record"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO fairness_checks (
                        grievance_id, decision_id, similar_cases,
                        consistency_score, anomaly_detected, demographic_parity
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    str(grievance_id),
                    str(decision_id) if decision_id else None,
                    Json(similar_cases),
                    consistency_score,
                    anomaly_detected,
                    Json(demographic_parity) if demographic_parity else None
                ))
                
                check_id = cur.fetchone()[0]
                logger.info(f"Created fairness check {check_id} for grievance {grievance_id}")
                return check_id
    
    # ==================== Utility Methods ====================
    
    def close(self):
        """Close all database connections"""
        if self.pool:
            self.pool.closeall()
            logger.info("Database connection pool closed")


# Singleton instance
_db_service: Optional[DatabaseService] = None


def get_database_service() -> DatabaseService:
    """Get or create database service instance"""
    global _db_service
    if _db_service is None:
        _db_service = DatabaseService()
    return _db_service
