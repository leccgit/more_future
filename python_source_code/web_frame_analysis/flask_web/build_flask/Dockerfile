FROM python:3.7-alpine
RUN mkdir /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
WORKDIR /code
ENV PYTHONPATH=/code
#ENV FLASK_APP app.py
#ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000
CMD ["python", "app.py"]