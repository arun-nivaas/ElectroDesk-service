from fastapi import APIRouter

v2_router = APIRouter(prefix="/api/v2")

# When v2 routes are ready, import and mount them here.
# They will reuse api/dependencies/ without any duplication.