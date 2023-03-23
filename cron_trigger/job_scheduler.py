from typing import List, Optional

from apscheduler.schedulers.tornado import TornadoScheduler

from cron_trigger.job_node import JobNode

__all__ = [
    "CronJobCollection"
]


class CronJobCollection:
    def __init__(self):
        self._scheduler = TornadoScheduler()
        self._task_context: [str, JobNode] = {}

    def context_get_job(self, job_id: str) -> Optional[JobNode]:
        return self._task_context.get(job_id)

    def context_add_job(self, new_job: JobNode):
        job_id = new_job.job_id
        if not new_job.is_job_valid():
            self.context_remove_job(job_id)
            return
        old_job = self.context_get_job(job_id)
        if not old_job:
            self._upsert_job(new_job)
        elif old_job and new_job.is_job_change(old_job):
            self._upsert_job(new_job)

    def _upsert_job(self, job: JobNode):
        self._scheduler.add_job(job.job_func, **job.job_kwargs(), replace_existing=True)
        self._task_context.update({
            job.job_id: job
        })

    def context_remove_job(self, job_id: str):
        if self.context_get_job(job_id):
            try:
                self._task_context.pop(job_id, None)
                self._scheduler.remove_job(job_id)
            except Exception as e:
                pass
            print("【{}】remove job...".format(job_id))

    def scheduler_start(self):
        self._scheduler.start()
        self.cron_check_trigger_jobs()
        self.context_add_job(
            JobNode(
                self.cron_check_trigger_jobs,
                id="cron_check_trigger_jobs",
                trigger="cron",
                is_permanent=True,
                day_of_week="*",
                hour="*",
                minute="*",
                second="25"
            )
        )

    def cron_check_trigger_jobs(self):
        try:
            next_cron_jobs = self.get_all_trigger_funcs()
            valid_job_ids = [cron_job.job_id for cron_job in next_cron_jobs]
            # 内存中已经注册的定时任务
            for m_job in self.pick_context_jobs():
                if m_job.is_job_permanent():
                    continue
                if m_job.job_id not in valid_job_ids:
                    self.context_remove_job(m_job.job_id)

            # seq2: 注册新的定时任务
            for valid_task in next_cron_jobs:
                self.context_add_job(valid_task)
            print(
                "cron_check_trigger_jobs task end, valid task:{}".format(
                    self.pick_context_job_ids()))
        except Exception as e:
            pass

    def get_all_trigger_funcs(self, **kwargs) -> List[JobNode]:
        raise NotImplementedError

    def pick_context_jobs(self) -> List[JobNode]:
        return list(self._task_context.values())

    def pick_context_job_ids(self) -> List[str]:
        return list(self._task_context.keys())
