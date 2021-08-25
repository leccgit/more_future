"""
    添加请求的全局对象
"""
import time
from werkzeug import Response as BaseResponse, Request as RequestBase
from werkzeug.local import LocalStack, LocalProxy
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException


class Response(BaseResponse):
    pass


class Request(RequestBase):
    pass


class _RequestContext(object):
    def __init__(self, wsgi_app, environ):
        self.app = wsgi_app
        # 上下文对象的url_adapter属性通过Flask应用中的Map实例构造成一个MapAdapter实例
        # 主要功能是将请求中的URL和Map实例中的URL规则进行匹配
        self.url_adapter = wsgi_app.url_map.bind_to_environ(environ)
        self.request = wsgi_app.request_class(environ)

    def __enter__(self):
        _request_ctx_stack.push(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            _request_ctx_stack.pop()


class Flask_03(object):
    """记录请求耗时"""
    response_class = Response
    request_class = Request

    def __init__(self):
        self.wsgi_app = self.wsgi_app
        self.view_functions = {}  # 路由装饰函数
        self.url_map = Map()
        self.error_handlers = {}
        self.before_request_func = []  # 前置请求
        self.after_request_func = []  # 后置请求
        self.debug = False

    def errorHandlers(self, code):
        """
        添加指定状态码的错误处理
        :param code:
        :return:
        """

        def decorator(f):
            self.error_handlers[code] = f

        return decorator

    def route(self, rule, **options):
        """
        添加路由装饰器和路由装饰函数
        等价于 self.view_function[] = xx
        :param rule:
        :param options:
        :return:
        """

        def decorator(f):
            self.add_url_rule(rule, f.__name__, **options)
            self.view_functions[f.__name__] = f
            return f

        return decorator

    def add_url_rule(self, rule, endpoint, **options):
        options['endpoint'] = endpoint
        options.setdefault('methods', ('GET',))
        self.url_map.add(Rule(rule, **options))

    def before_request(self, f):
        """注册一个函数, 在每个请求前置执行"""
        self.before_request_func.append(f)
        return f

    def after_request(self, f):
        """注册一个函数, 在每个请求后置执行"""
        self.after_request_func.append(f)
        return f

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
        with self.request_context(environ):
            dispatch_result = self.preprocess_request()
            if dispatch_result is None:
                dispatch_result = self.dispatch_request()
            response = self.make_response(dispatch_result)
            response = self.process_response(response)
            return response(environ, start_response)

    def request_context(self, environ):
        """
        创建请求对象
        :return:
        """
        return _RequestContext(self, environ)

    def preprocess_request(self):
        """ 执行所有的前置请求 """
        for pre_func in self.before_request_func:
            rv = pre_func()
            if rv is not None:
                return rv

    def process_response(self, response):
        """ 针对响应执行所有的后置请求 """
        for handler in self.after_request_func:
            response = handler(response)
        return response

    def dispatch_request(self):
        """
        针对调度的路由, 执行对应视图函数的执行方法
        :return:
        """
        try:
            endpoint, values = self.match_request()
            return self.view_functions[endpoint](**values)
        except HTTPException as e:
            handler = self.error_handlers.get(e.code)
            if handler is None:
                return e
            else:
                return handler(e)
        except Exception as e:
            handler = self.error_handlers.get(500)
            if self.debug or handler is None:
                raise
            return handler(e)

    def match_request(self):
        """
        匹配对应的路由规则
        :return:
        """
        rv = _request_ctx_stack.top.url_adapter.match()
        return rv

    def make_response(self, rv):
        if isinstance(rv, str):
            return self.response_class(rv)
        if isinstance(rv, tuple):
            return self.response_class(*rv)
        return self.response_class.force_type(rv, request.environ)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


_request_ctx_stack = LocalStack()
request = LocalProxy(lambda: _request_ctx_stack.top.request)
current_app = LocalProxy(lambda: _request_ctx_stack.top.app)

if __name__ == '__main__':
    app = Flask_03()


    @app.errorHandlers(404)
    def page_note_found(error):
        return "This page does not exist', 404"


    @app.errorHandlers(500)
    def page_note_found(error):
        return "Server error', 500"


    def add_before_request():
        print('路由前置判断进入!')


    app.before_request(add_before_request)


    @app.route('/name')
    def make_index():
        print('this is index test!')
        print(_request_ctx_stack._local.__storage__)
        return 'make_index'


    app.run()
