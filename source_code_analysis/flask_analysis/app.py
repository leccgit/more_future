import time
from pprint import pprint


class FlaskStudy(object):
    """记录请求耗时"""

    def __init__(self):
        self.wsgi_app = self.wsgi_app

    def run(self, host='127.0.0.1', port=5000, **options):
        from werkzeug import run_simple
        return run_simple(host, port, self, **options)

    def wsgi_app(self, environ, start_response):
        """
        web服务器在将请求转交给web应用程序之前，需要先将http报文转换为WSGI规定的格式
        :param environ: 字典，包含请求的所有信息
        :param start_response: 在可调用对象中调用的函数，用来发起响应，参数包括状态码，headers等
        :return:
        """
        start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8'), ('Server', 'google')])
        pprint(environ)
        return_body = ["\nHello WSGI!"]  # 返回结果必须是bytes
        return ["\n".join(return_body).encode("utf-8")]

    def __call__(self, environ, start_response):
        start_time = time.time()
        response = self.wsgi_app(environ, start_response)
        response_time = (time.time() - start_time) * 1000
        timing_text = "记录请求耗时中间件输出\n\n本次请求耗时: {:.10f}ms \n\n\n".format(response_time)
        response.append(timing_text.encode('utf-8'))
        return response


app = FlaskStudy()
app.run()  # 0.0.0.0: 告诉操作系统监听所有公开的IP, 默认的127.0.0.1只能本地访问
