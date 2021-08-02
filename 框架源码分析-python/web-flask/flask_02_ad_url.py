import time
from pprint import pprint
from werkzeug import Response as BaseResponse


class Response(BaseResponse):
    pass


class Flask_02(object):
    """记录请求耗时"""
    response_class = Response

    def __init__(self):
        self.wsgi_app = self.wsgi_app
        self.view_functions = {}  # 路由装饰函数

    def route(self, rule, endpoint, **options):
        """
        添加路由装饰器
        等价于 self.view_function[] = xx
        :param rule:
        :param endpoint:
        :param options:
        :return:
        """
        def decorator(f):
            self.add_url(rule, endpoint, **options)
            return f

        return decorator

    def add_url(self, rule, endpoint, **options):
        pass

    def run(self, host='127.0.0.1', port=8080, **options):
        from werkzeug import run_simple
        return run_simple(host, port, self, **options)

    def wsgi_app(self, environ, start_response):
        """
        web服务器在将请求转交给web应用程序之前，需要先将http报文转换为WSGI规定的格式
        :param environ: 字典，包含请求的所有信息
        :param start_response: 在可调用对象中调用的函数，用来发起响应，参数包括状态码，headers等
        :return:
        """
        pprint(environ)
        return_body = ["\nHello WSGI!"]  # 返回结果必须是bytes
        response = self.make_response(*return_body)
        return response(environ, start_response)

    def make_response(self, rv):
        if isinstance(rv, str):
            return self.response_class(rv)
        if isinstance(rv, tuple):
            return self.response_class(*rv)
        print('参数错误！')

    def __call__(self, environ, start_response):
        # start_time = time.time()
        # # response =
        # # pprint(response)
        # response_time = (time.time() - start_time) * 1000
        # timing_text = "记录请求耗时中间件输出\n\n本次请求耗时: {:.10f}ms \n\n\n".format(response_time)
        # response.append(timing_text.encode('utf-8'))
        return self.wsgi_app(environ, start_response)


if __name__ == '__main__':
    app = Flask_02()
    app.run()
