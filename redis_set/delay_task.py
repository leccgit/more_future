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
        "start_time": "1609632212",
        "end_time": "1689673212",
        "trigger_type": "cron",
        "is_permanent": 0,
        # "trigger_sections": ["09:00", "03:00"]
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
        self.trigger_type = self.content.get("trigger_type")
        self.is_permanent = bool(self.content.get("is_permanent"))
        self.trigger_sections = self.content.get("trigger_sections") or []
        if self.content.get("start_time"):
            st_timestamp = int(self.content["start_time"])
            self.start_time = datetime.fromtimestamp(st_timestamp)
        else:
            self.start_time = None

        if self.content.get("end_time"):
            ed_timestamp = int(self.content["end_time"])
            self.end_time = datetime.fromtimestamp(ed_timestamp)
        else:
            self.end_time = None

    def get_jid(self):
        return self._job_id

    def get_score(self):
        return self._job_score

    def is_valid(self) -> bool:
        if self.is_permanent:
            return True
        return self.cron_in_time_section(now_time(), self.start_time, self.end_time)

    def next_trigger_time(self) -> int:
        try:
            if self.trigger_type == TriggerType.cron:
                # 周期执行
                trigger_time = None
                if self.trigger_index + 1 <= len(self.trigger_sections):
                    trigger_time_str = self.trigger_sections[self.trigger_index]
                    if len(trigger_time_str) == 5:
                        trigger_time = datetime.strptime(trigger_time_str, "%H:%M")
                    if len(trigger_time_str) == 8:
                        trigger_time = datetime.strptime(trigger_time_str, "%H:%M:%S")
                if trigger_time is None:
                    return 0
                n_time = now_time()
                c_trigger_time = datetime(
                    n_time.year, n_time.month, n_time.day, trigger_time.hour,
                    trigger_time.minute, trigger_time.second) + timedelta(days=1)
                if self.cron_in_time_section(c_trigger_time, self.start_time, self.end_time):
                    return (c_trigger_time - n_time).seconds
                return 0
            if self.trigger_type == TriggerType.interval:
                pass
            return 0
        except Exception as e:
            print("parse next_trigger_time error:{}".format(str(e)))
            return 0

    @staticmethod
    def cron_in_time_section(check_time: datetime, start_time: datetime, end_time: datetime) -> bool:
        """
        通过时间区间判断任务是否有效
        :param check_time:
        :param start_time:
        :param end_time:
        :return:
        """
        if not start_time and not end_time:
            return True
        if start_time and end_time:
            return start_time <= check_time <= end_time
        if start_time:
            return start_time <= check_time
        if end_time:
            return check_time <= end_time
        return False


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

    def put(self, key: str, delay: int, **kwargs) -> int:
        """
        将任务推送入列
        :param key:
        :param delay: 延迟的秒数
        :param kwargs:
        :return:
        """
        score = get_now_timestamp() + delay
        print("put key:{}, delay:{} trigger_time:{}".format(key, delay, datetime.fromtimestamp(score)))
        put_result = self.connection.zadd(self._que_name, {key: score}, **kwargs)
        return put_result

    def delete(self, key) -> int:
        del_result = self.connection.zrem(self._que_name, key)
        print("delete key:{}, trigger_time:{}".format(key, now_time()))
        return del_result

    def peek_ready(self, ttr: int, num: int = None, withscores: bool = True, **kwargs) -> List[Tuple[str, int]]:
        """
        获取最近待过期的任务
        :param ttr:
        :param num:
        :param withscores:
        :param kwargs:
        :return:
        """
        max_score = get_now_timestamp()
        min_score = max_score - ttr
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
        self.check_ttr = 60 * 3  # 允许的延迟时间

    def start(self, conn: Redis):
        self.delay_bucket.init_self(conn)
        self.job_store.init_self(conn)

    def ready_que(self, ttr: int = None) -> List[JobMate]:
        ttr = ttr or self.check_ttr
        ready_job = self.delay_bucket.peek_ready(ttr)
        if not ready_job:
            return []
        job_mates = self.job_store.get_job_mates(ready_job)
        return job_mates

    def process_task(self, job_mate: JobMate):
        job_id = job_mate.get_jid()
        if job_mate.is_valid():
            del_suc = self.delay_bucket.delete(job_id)
            if del_suc:
                # TODO: 在该处, 没有做失败重试的操作, 因为该处的失败，重试还是失败，重试没有意义
                self.do_trigger_func(job_mate)
            next_trigger_time = job_mate.next_trigger_time()
            if next_trigger_time:
                self.delay_bucket.put(job_id, next_trigger_time)
            return
        else:
            self.delay_bucket.delete(job_id)
            return

    def do_trigger_func(self, job_mate):
        print("TimerScheduler[{}] do...".format(datetime.now()))


if __name__ == '__main__':
    import time

    _redis = Redis(
        host='124.223.182.33',
        port=6379,
        db=0,
        password="Leichao2022")
    _timer = TimerScheduler(que_name="delay_bucket")
    _timer.start(_redis)
    # _timer.delay_bucket.put("xc_ebike_2_config_AutoChangeBattrey_1916", 1)
    for i in range(10):
        _timer.delay_bucket.put("{}~~~xc_ebike_2_config_AutoChangeBattrey_1916~~~0".format(i), i)

    # 1679628496
    while True:
        read_tasks = _timer.ready_que()
        if read_tasks:
            for r_job in read_tasks:
                _timer.process_task(r_job)
        time.sleep(0.01)
