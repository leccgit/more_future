from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

from redis import Redis
from redis.typing import ZScoreBoundT


class TriggerType:
    cron = "cron"  # 定时
    interval = "interval"  # 周期


def to_str(bytes_or_str) -> str:
    """
    byte转string
    :param bytes_or_str:
    :return:
    """
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode("utf-8")
    else:
        value = bytes_or_str
    return value


def trace_datetime_from_stamp(c_timestamp: int = None) -> Optional[datetime]:
    if not c_timestamp:
        return None
    st_timestamp = int(c_timestamp)
    try:
        return datetime.fromtimestamp(st_timestamp)
    except Exception as e:
        return None


def now_time():
    return datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")


def get_timestamp(c_time: datetime) -> int:
    """
    获取输入时间的秒数
    :param c_time:
    :return:
    """
    return int(round(c_time.timestamp()))


def get_now_timestamp() -> int:
    """
    获取当前时间的秒数
    :return:
    """
    return get_timestamp(now_time())


def set_job_id(service_id: str, router: str, trigger_index: int = 0) -> str:
    return "{}~~~{}~~~{}".format(service_id, router, trigger_index)


def parse_job_id(job_id: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    service_id = None
    router = None
    trigger_index = None
    parse_id = job_id.split("~~~")
    if parse_id and len(parse_id) == 3:
        service_id = parse_id[0]
        router = parse_id[1]
        trigger_index = parse_id[2]
    return service_id, router, trigger_index


def get_job_raw_context(router: str, service_id: str) -> Dict:
    return {
        "task_name": "活动名称",

        # 确定任务是否有效
        "is_permanent": 0,  # 是否永久任务 0： false, 1: true
        "is_once": 0,  # 是否执行一次 0： false, 1: true
        "start_time": "1609632212",  # 开始时间
        "end_time": "1689673212",  # 接受时间

        # 调度任务类型
        "trigger_type": "cron",
        # 任务调度参数
        # ["09:00", "03:00"], 表示在几点进行执行，暂时不支持解析复杂参数，
        # 如果是interval，那么该处为执行时间的秒数 [100]
        "trigger_args": [],
        # 任务执行参数，按业务而定
        "exec_kwargs": {

        }
    }


class JobMate:
    """
    任务执行的元信息
    """

    def __init__(
            self,
            job_id: str,
            job_score: int,
            content: Dict = None,
    ):
        self._job_id = job_id
        self._job_score = job_score
        s_sid, s_router, s_index = parse_job_id(job_id)
        self.service_id = s_sid
        self.router = s_router
        self.trigger_index = int(s_index or 0)
        self.content = content or {}

        # context 配置解析
        self.task_name = self.content.get("task_name")
        # 调度执行参数
        self.is_once = bool(self.content.get("is_once"))
        self.is_permanent = bool(self.content.get("is_permanent"))
        # 调度任务类型
        self.trigger_type = self.content.get("trigger_type")
        self.trigger_args = self.content.get("trigger_args") or []
        # 任务开始时间区间
        self.start_time = trace_datetime_from_stamp(self.content.get("start_time"))
        self.end_time = trace_datetime_from_stamp(self.content.get("end_time"))
        # 任务执行参数, 字典结构
        self.exec_kwargs = self.content.get("exec_kwargs") or {}

    def get_jid(self) -> str:
        return self._job_id

    def get_score(self) -> int:
        return int(self._job_score)

    def exec_once(self) -> bool:
        """
        是否执行一次
        :return: 
        """
        return bool(self.is_once)

    def exec_permanent(self) -> bool:
        """
        是否永久执行
        :return: 
        """
        return bool(self.is_permanent)

    def exec_time_in_work_section(
            self, exec_time: datetime,
    ) -> bool:
        """
        通过时间区间判断任务是否有效
        :param exec_time:
        :return:
        """
        if not self.start_time and not self.end_time:
            return True
        if self.start_time and self.end_time:
            return self.start_time <= exec_time <= self.end_time
        if self.start_time:
            return self.start_time <= exec_time
        if self.end_time:
            return exec_time <= self.end_time
        return False

    def next_trigger_score(self) -> int:
        try:
            if self.trigger_type == TriggerType.cron:
                return self._get_cron_next_trigger_score()
            if self.trigger_type == TriggerType.interval:
                return self._get_interval_next_trigger_score()
            return 0
        except Exception as e:
            print("parse next_trigger_score error:{}".format(str(e)))
            return 0

    def _get_cron_next_trigger_score(self) -> int:
        if self.is_once:
            # 当前任务只执行一次, 下一执行的分值为0
            return 0

        trigger_time = None
        if self.trigger_index + 1 <= len(self.trigger_args):
            trigger_time_str = self.trigger_args[self.trigger_index]
            if len(trigger_time_str) == 5:
                trigger_time = datetime.strptime(trigger_time_str, "%H:%M")
            if len(trigger_time_str) == 8:
                trigger_time = datetime.strptime(trigger_time_str, "%H:%M:%S")
        if trigger_time is None:
            return 0
        n_time = now_time()
        n_trigger_time = datetime(
            n_time.year, n_time.month, n_time.day, trigger_time.hour,
            trigger_time.minute, trigger_time.second) + timedelta(days=1)
        if self.is_permanent:
            # 当前为永久任务
            return get_timestamp(n_trigger_time)
        if self.exec_time_in_work_section(n_trigger_time):
            # 当前任务在指定时间内
            return get_timestamp(n_trigger_time)
        return 0

    def _get_interval_next_trigger_score(self) -> int:
        if self.is_once:
            # 当前任务只执行一次, 下一执行的分值为0
            return 0
        trigger_seconds = None
        if self.trigger_index + 1 <= len(self.trigger_args):
            trigger_seconds = int(self.trigger_args[self.trigger_index])
        if trigger_seconds is None:
            return 0
        n_trigger_time = now_time() + timedelta(seconds=trigger_seconds)
        if self.is_permanent:
            # 当前为永久任务
            return get_timestamp(n_trigger_time)
        if self.exec_time_in_work_section(n_trigger_time):
            # 当前任务在指定时间内
            return get_timestamp(n_trigger_time)
        return 0


class JobStore:
    """
    任务元信息集合
    """

    def __init__(self, ):
        self.connection: Optional[Redis] = None
        self._job_mates = []

    def init_self(self, conn: Redis):
        self.connection = conn

    def get_job_mates(self, job_info: List[Tuple[str, int]]) -> List[JobMate]:
        self._job_mates = []
        for j_tuple in job_info:
            j_id, j_score = j_tuple
            s_sid, s_router, s_index = parse_job_id(j_id)
            job_context = get_job_raw_context(s_sid, s_router)
            self._job_mates.append(JobMate(j_id, j_score, content=job_context))
        return self._job_mates


class DelayBucket:
    """
    延迟队列
    """

    def __init__(self, que_name: str):
        self._que_name = que_name
        self.connection: Optional[Redis] = None

    def init_self(self, conn: Redis):
        self.connection = conn

    def put(self, key: str, score: int, **kwargs) -> int:
        """

        :param key:
        :param score: 延迟的秒数
        :param kwargs:
        :return:
        """
        print("put key:{}, trigger_time:{}".format(key, datetime.fromtimestamp(score)))
        put_result = self.connection.zadd(self._que_name, {key: score}, **kwargs)
        return put_result

    def delete(self, key) -> int:
        del_result = self.connection.zrem(self._que_name, key)
        print("delete key:{}, trigger_time:{}".format(key, now_time()))
        return del_result

    def peek_ready(self, num: int = None, withscores: bool = True, **kwargs) -> List[Tuple[str, int]]:
        """

        :param num:
        :param withscores:
        :param kwargs:
        :return:
        """
        max_score = get_now_timestamp()
        min_score = 0
        peek_result = self.get_range(min_score, max_score, num=num, withscores=withscores, **kwargs)
        return peek_result

    def get_range(
            self,
            min_score: ZScoreBoundT,
            max_score: ZScoreBoundT,
            num: int = None,
            withscores: bool = True,
            **kwargs
    ) -> List[Tuple[str, int]]:
        read_task = self.connection.zrangebyscore(
            self._que_name, min=min_score, max=max_score,
            num=num, withscores=withscores, **kwargs)
        get_result = []
        for j_id, j_score in read_task:
            get_result.append((to_str(j_id), int(j_score)))
        return get_result


class TimerScheduler:
    """
    执行调度
    """

    def __init__(self, que_name: str):
        self.delay_bucket = DelayBucket(que_name)
        self.job_store = JobStore()

    def init_self(self, conn: Redis):
        self.delay_bucket.init_self(conn)
        self.job_store.init_self(conn)

    def run_forever(self):
        # TODO: 改成定时任务
        while True:
            read_tasks = self.ready_que()
            if read_tasks:
                for r_job in read_tasks:
                    self.process_task(r_job)
            time.sleep(0.01)

    def ready_que(self) -> List[JobMate]:
        ready_job = self.delay_bucket.peek_ready()
        if not ready_job:
            return []
        job_mates = self.job_store.get_job_mates(ready_job)
        return job_mates

    def process_task(self, job_mate: JobMate):
        # 执行时间，是通过分值来转换的
        exec_time = trace_datetime_from_stamp(job_mate.get_score())
        try:
            job_id = job_mate.get_jid()
            # seq1: 先注册下一周期的任务, 避免任务注册异常问题
            next_score = 0
            if job_mate.exec_once():
                pass
            elif job_mate.exec_permanent():
                next_score = job_mate.next_trigger_score()
            elif job_mate.exec_time_in_work_section(exec_time):
                next_score = job_mate.next_trigger_score()
            if next_score:
                self.delay_bucket.put(job_id, next_score)

            # seq2: 进行数据删除逻辑，删除成功，则执行后续的业务逻辑
            del_suc = self.delay_bucket.delete(job_id)
            if not del_suc:
                # zset本身的delete就具备分布式逻辑
                return
            # 如果任务失败，在该处没有重试
            self.do_trigger_func(job_mate)

        except Exception as e:
            print("process_task fail, error:{}".format(str(e)))

    @staticmethod
    def do_trigger_func(job_mate):
        # TODO: 在该处, 没有做失败重试的操作, 因为该处的失败，重试还是失败，重试没有意义
        print("TimerScheduler[{}] do...".format(datetime.now()))
        return


def start_timer_scheduler():
    _timer = TimerScheduler(que_name="delay_bucket")
    _timer.init_self(Redis(
        host='124.223.182.33',
        port=6379,
        db=0,
        password="Leichao2022"))
    for i in range(10):
        _timer.delay_bucket.put("{}~~~xc_ebike_2_config_AutoChangeBattrey_1916~~~0".format(i), get_now_timestamp() + i)

    _timer.run_forever()


if __name__ == '__main__':
    """
    服务区 + router + index 被标记为一个唯一任务
    """
    import time

    start_timer_scheduler()
