from src.celery_tasks.tasks_hello import send_celery_msg

result = send_celery_msg.delay("yuan")
print(result.id)
result2 = send_celery_msg.delay("alex")
print(result2.id)
print(result)
