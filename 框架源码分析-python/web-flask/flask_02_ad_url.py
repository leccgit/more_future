from werkzeug import Response as BaseResponse, Request as RequestBase
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException


class Response(BaseResponse):
    pass


class Flask_02(object):
    """记录请求耗时"""
    response_class = Response

    def __init__(self):
        self.wsgi_app = self.wsgi_app
        self.view_functions = {}  # 路由装饰函数
        self.url_map = Map()
        self.error_handlers = {}

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
        url_adapter = self.url_map.bind_to_environ(environ)
        try:
            # 通过环境变量,找到对应的视图函数,并进行执行
            endpoint, values = url_adapter.match()
            result = self.view_functions[endpoint](**values)
        except HTTPException as e:
            handler = self.error_handlers.get(e.code)
            if handler is None:
                result = e
            else:
                result = handler(e)
        response = self.make_response(result, environ)
        return response(environ, start_response)

    def make_response(self, rv, environ):
        if isinstance(rv, str):
            return self.response_class(rv)
        if isinstance(rv, tuple):
            return self.response_class(*rv)
        return self.response_class.force_type(rv, environ)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


if __name__ == '__main__':
    app = Flask_02()


    @app.errorHandlers(404)
    def page_note_found(error):
        return "This page does not exist', 404"


    @app.route('/name')
    def make_index():
        print('this is index test!')
        return 'make_index'


    app.run()
    print(app.url_map)
