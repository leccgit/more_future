import requests

url = "https://way.jd.com/jisuapi/byclass?classid=625&start=0&num=10&appkey=77e9d3544f042837fafeefdae807aa4d"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
