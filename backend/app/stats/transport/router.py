from fastapi import APIRouter

from ..models import StatsResponse
from .me import me_stats_endpoint

router = APIRouter(prefix="/stats", tags=["stats"])

router.add_api_route(
    path="/me",
    endpoint=me_stats_endpoint,
    methods=["GET"],
    response_model=StatsResponse,
)
