from src.celery_tasks.task_with_mg import compute_process_single_with_celery

result = compute_process_single_with_celery.delay()
print(result.id)
print(result.get())