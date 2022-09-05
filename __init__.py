# import time
# import requests
#
# while True:
#     url = "http://127.0.0.1:8080/api/user/"
#
#     payload = {}
#     # headers = {
#     #     # 'x-request-id': 'daa8575b66024881aff69e8ef9c0b62a'
#     # }
#
#     response = requests.request("GET", url, data=payload)
#
#     print(response.text)
#     time.sleep(.01)
if __name__ == '__main__':
    import asyncio

    current_loop = asyncio.get_event_loop()


    async def print_time(loop):
        start_time = loop.time()
        await asyncio.sleep(2)
        print(loop.time() - start_time)


    current_loop.run_until_complete(print_time(current_loop))
    current_loop.close()
