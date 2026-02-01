"""
Configuration management for Academic Grievance DSS Backend
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "Academic Grievance DSS"
    app_version: str = "1.0.0"
    debug_mode: bool = True
    log_level: str = "INFO"
    
    # Server
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "grievance_db"
    postgres_user: str = "grievance_user"
    postgres_password: str = "grievance_password"
    
    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def async_database_url(self) -> str:
        """Construct async PostgreSQL connection URL"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # OpenAI / LLM
    openai_api_key: str
    openai_model: str = "gpt-4-turbo"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.3
    
    # Drools
    drools_rules_path: str = "./rules"
    drools_log_level: str = "INFO"
    java_home: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Testing
    test_database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Dependency injection for FastAPI"""
    return settings
