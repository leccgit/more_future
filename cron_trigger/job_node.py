from collections import Callable
from datetime import datetime
from typing import Dict
from uuid import uuid4

__all__ = [
    "JobNode"
]


class JobNode:
    def __init__(
            self,
            func: Callable,
            id: str = None,
            task_timestamp: str = None,
            trigger=None,
            start_time: datetime = None,
            end_time: datetime = None,
            args=None,
            kwargs=None,
            name=None,
            is_permanent: bool = False,
            **trigger_args
    ):
        self.func = func
        self.id = id or str(uuid4())
        self.task_timestamp = task_timestamp
        self.trigger = trigger
        self.start_time = start_time
        self.end_time = end_time
        self.args = tuple(args) if args is not None else ()
        self.kwargs = dict(kwargs) if kwargs is not None else {}
        self.name = name
        self.trigger_args = trigger_args
        self.is_permanent = is_permanent

    def is_job_permanent(self) -> bool:
        return bool(self.is_permanent)

    @property
    def job_id(self) -> str:
        return self.id

    @property
    def job_func(self) -> Callable:
        return self.func

    def job_kwargs(self) -> Dict:
        return {
            'trigger': self.trigger,
            'args': self.args,
            'kwargs': self.kwargs,
            'id': self.job_id,
            'name': self.name,
            **self.trigger_args
        }

    def is_job_change(self, other_job) -> bool:
        return self.task_timestamp != other_job.task_timestamp

    def is_job_valid(self) -> bool:
        """
        判断任务是否有效
        :return:
        """
        if self.is_job_permanent():
            return True

        # 通过时间区间判断任务是否有效
        if not self.start_time and not self.end_time:
            return True
        if self.start_time and self.end_time:
            return self.start_time <= self.now_time() <= self.end_time
        if self.start_time:
            return self.start_time <= self.now_time()
        if self.end_time:
            return self.now_time() <= self.end_time
        return False

    @staticmethod
    def now_time() -> datetime:
        return datetime.now()

    def __repr__(self):
        return str(self.job_kwargs())
