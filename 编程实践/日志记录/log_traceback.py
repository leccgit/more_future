"""
try:
    do_something()
except:
    pass
exception中, 有用的错误信息都被隐藏, 避免当生产中出现问题, 难以定位问题, 需要将有用的日志信息进行记录
"""
import traceback
from functools import partial


def log_traceback(ex, logger_handle=None, ex_traceback=None):
    """

    :param ex:
    :param logger_handle: 日志记录对象, 代码层次自己实现
    :param ex_traceback: py2的代码兼容
    :return:
    """
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = "".join(traceback.format_exception(ex.__class__, ex, ex_traceback))
    if not logger_handle:
        logger_handle = print
    logger_handle(tb_lines)


def log_traceback_1(ex, logger_handle=None, ex_traceback=None):
    """

    :param ex:
    :param logger_handle: 日志记录对象, 代码层次自己实现
    :param ex_traceback: py2的代码兼容
    :return:
    """
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [line.replace("\n", "&&") for line in
                traceback.format_exception(ex.__class__, ex, ex_traceback)]
    if not logger_handle:
        logger_handle = print
    logger_handle(''.join(tb_lines))


py3_error_traceback = partial(log_traceback_1, logger_handle=print, ex_traceback=None)

if __name__ == '__main__':
    try:
        result = 1 / 0
    except Exception as e:
        log_traceback(e)
