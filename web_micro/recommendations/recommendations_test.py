from recommendations import RecommendationService
from recommendations_pb2 import BookCategory, RecommendationRequest


def test_recommendations():
    service = RecommendationService()
    request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=3
    )
    response = service.Recommend(request, None)
    assert len(response.recommendations) == 3


if __name__ == '__main__':
    test_recommendations()
