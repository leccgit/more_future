from src.celery_hello.celery_to_hello import send_msg

result = send_msg.delay("yuan")
print(result.id)
result2 = send_msg.delay("alex")
print(result2.id)
print(result)