from typing import List

from cron_trigger.job_node import JobNode
from cron_trigger.job_scheduler import CronJobCollection


def trigger_func(*args, **kwargs):
    print("[{}]: trigger_func register, haha.".format(kwargs.get("task_id")))


_item = {
    "id": "任务唯一id",
    "task_timestamp": "任务创建时间戳",
    "trigger": "触发类型",  # cron, interval
    "start_time": "任务计划开始时间",  # datetime
    "end_time": "任务计划完成时间",  # datetime
    "is_permanent": "是否为永久任务",
    "trigger_args": {},  # 周期函数参数
}
# 定时
_corn_args = {
    "day_of_week": "*",
    "hour": "*",
    "minute": "*",
    "second": "25"
}

#
_interval_args = {
    "seconds": "25",
}


class MemoryJob(CronJobCollection):
    def get_all_trigger_funcs(self) -> List[JobNode]:
        cron_tasks = []
        for i in range(10):
            task_id = str(i)
            cron_tasks.append(
                JobNode(
                    trigger_func,
                    id=task_id,
                    trigger="interval",
                    kwargs={"task_id": task_id},
                    seconds=1
                )
            )
        if cron_tasks:
            cron_tasks = [
                task for task in cron_tasks if task.is_job_valid()
            ]
        return cron_tasks


if __name__ == '__main__':
    import asyncio

    MemoryJob().scheduler_start()
    current_loop = asyncio.get_event_loop()
    current_loop.run_forever()
