import os

from flask import Flask, jsonify
import grpc

from recommendations_pb2_grpc import RecommendationsStub
from recommendations_pb2 import RecommendationRequest, BookCategory

app = Flask(__name__)

recommendations_host = os.getenv("RECOMMENDATIONS_HOST", "localhost")
recommendations_channel = grpc.insecure_channel(
    f"{recommendations_host}:50051"
)
recommendations_client = RecommendationsStub(recommendations_channel)


@app.route("/")
def render_homepage():
    recommendations_request = RecommendationRequest(
        user_id=1, category=BookCategory.MYSTERY, max_results=3
    )
    recommendations_response = recommendations_client.Recommend(
        recommendations_request
    )
    print(recommendations_response)
    print(type(recommendations_response))
    return str(recommendations_response)


if __name__ == '__main__':
    app.run()
