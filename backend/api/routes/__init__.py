"""
API routes package
"""
from .grievances import router as grievances_router
from .decisions import router as decisions_router
from .metadata import router as metadata_router

__all__ = ["grievances_router", "decisions_router", "metadata_router"]
