from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)
import recommendations_pb2_grpc

from grpc_interceptor import ServerInterceptor

# 模拟数据库中的数据
books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(
            id=4, title="The Hitchhiker's Guide to the Galaxy"
        ),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(
            id=7, title="The 7 Habits of Highly Effective People"
        ),
        BookRecommendation(
            id=8, title="How to Win Friends and Influence People"
        ),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
    ],
}


class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        """
        必须与在 protobuf 文件中定义的 RPC 具有相同的名称
        :param request:
        :param context:
        :return:
        """
        if request.category not in books_by_category:
            # context上下文参数, 允许设置响应的状态码
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)


def serve():
    class ErrorLogger(ServerInterceptor):
        def intercept(self, method, request, context, method_name):
            try:
                return method(request, context)
            except Exception as e:
                self.log_error(e)
                raise

        def log_error(self, e: Exception) -> None:
            pass

    interceptors = [ErrorLogger()]
    # 创建gRPC服务器, 使用10个线程来处理请求
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors)
    # 将服务器和处理程序相关联
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    # 50051是gRPC的标准端口, 可以根据实际使用进行调整
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

