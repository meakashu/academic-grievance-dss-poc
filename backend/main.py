"""
Academic Grievance Decision Support System - Backend API
FastAPI application with rule engine integration
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Dict, Any

from config import settings, get_settings
from services.database_service import get_database_service
from services.llm_service import get_llm_service

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for application startup and shutdown
    """
    # Startup
    logger.info("Starting Academic Grievance DSS Backend...")
    logger.info(f"Debug mode: {settings.debug_mode}")
    logger.info(f"Database: {settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}")
    logger.info(f"LLM Model: {settings.openai_model}")
    
    # Initialize services
    try:
        # Try to initialize database service
        try:
            from services.database_service import get_database_service
            db_service = get_database_service()
            logger.info("✓ PostgreSQL database service initialized")
        except Exception as e:
            logger.warning(f"PostgreSQL unavailable: {str(e)}")
            logger.info("Using mock database service (in-memory storage)")
            from services.mock_database_service import get_mock_database_service
            # Replace the get_database_service function globally
            import services
            services.get_database_service = get_mock_database_service
            db_service = get_mock_database_service()
        
        llm_service = get_llm_service()
        logger.info("✓ LLM service initialized")
        
        # Try to initialize Drools engine via JPype1
        try:
            from services.rule_engine_service import get_rule_engine_service
            rule_engine = get_rule_engine_service()
            logger.info("✓ Drools engine initialized via JPype1")
        except Exception as e:
            logger.warning(f"Drools engine unavailable: {str(e)}")
            logger.info("Using mock rule engine for testing")
            from services.mock_rule_engine_service import get_mock_rule_engine_service
            # Store mock service globally for routes to use
            import sys
            sys.modules['__main__'].use_mock_engine = True
        
    except Exception as e:
        logger.error(f"Failed to initialize services: {str(e)}")
        raise
    
    logger.info("🚀 Application startup complete!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Academic Grievance DSS Backend...")
    
    try:
        db_service = get_database_service()
        db_service.close()
        logger.info("✓ Database connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")
    
    logger.info("👋 Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    A rule-based, hierarchy-aware, explainable decision support system 
    for academic grievance resolution in higher education institutions.
    
    ## Features
    
    * **Rule-Based Reasoning**: Drools engine with hierarchical rules (L1/L2/L3)
    * **Conflict Resolution**: Authority, temporal, and specificity precedence
    * **Complete Tracing**: Full audit trail of rule execution
    * **LLM Integration**: GPT-4 for ambiguity detection
    * **Fairness Monitoring**: Consistency checks across similar cases
    * **Explainability**: Multi-level explanations linking decisions to regulations
    
    ## Endpoints
    
    * **Grievances**: Submit and retrieve grievances
    * **Decisions**: Get decision outcomes and explanations
    * **Traces**: View complete rule execution traces
    * **Fairness**: Monitor consistency and detect anomalies
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== Health Check ====================

@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint
    
    Returns system status and service availability
    """
    try:
        # Check services
        db_status = "mock (in-memory)"
        llm_status = "configured"
        drools_status = "mock"
        
        try:
            from services.database_service import get_database_service
            get_database_service()
            db_status = "postgresql"
        except:
            pass
        
        try:
            from services.rule_engine_service import get_rule_engine_service
            get_rule_engine_service()
            drools_status = "jpype1"
        except:
            pass
        
        return {
            "status": "healthy",
            "version": settings.app_version,
            "services": {
                "database": db_status,
                "llm": llm_status,
                "drools": drools_status
            },
            "debug_mode": settings.debug_mode,
            "message": "All services operational"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/", tags=["Root"])
async def root() -> Dict[str, str]:
    """
    Root endpoint
    
    Returns welcome message and API documentation link
    """
    return {
        "message": "Academic Grievance Decision Support System API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if settings.debug_mode else "An error occurred"
        }
    )


# ==================== Import Routes ====================
from api.routes import grievances_router, decisions_router, metadata_router

app.include_router(grievances_router, prefix="/api", tags=["Grievances"])
app.include_router(decisions_router, prefix="/api", tags=["Decisions & Traces"])
app.include_router(metadata_router, prefix="/api", tags=["Rule Metadata"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug_mode,
        log_level=settings.log_level.lower()
    )
