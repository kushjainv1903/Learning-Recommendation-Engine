"""API route registration for LearnPath AI."""

import logging

from fastapi import APIRouter

from app.models.request_models import RecommendationRequest
from app.models.response_models import ErrorResponse, RecommendationResponse
from app.services.recommendation_engine import generate_learning_recommendations

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/recommend",
    response_model=RecommendationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Malformed JSON"},
        413: {"model": ErrorResponse, "description": "Payload too large"},
        415: {"model": ErrorResponse, "description": "Unsupported media type"},
        422: {"model": ErrorResponse, "description": "Validation failed"},
        500: {"model": ErrorResponse, "description": "Unexpected server error"},
    },
    summary="Generate learning recommendations",
)
def recommend(request: RecommendationRequest) -> RecommendationResponse:
    """Generate recommendations for one validated daily performance snapshot.

    Args:
        request: Validated recommendation request body.

    Returns:
        Serialized recommendation response.

    Raises:
        app.core.exceptions.RecommendationException: If the service pipeline fails.

    Example:
        >>> isinstance(recommend, object)
        True
    """
    logger.info("Recommendation request accepted for processing")
    response = generate_learning_recommendations(request)
    logger.info("Recommendation response generated")
    return response
