#FROM python:3.7-alpine
#RUN mkdir /code
#COPY requirements.txt /code/
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
#WORKDIR /code
#COPY . /code
#ENV PYTHONPATH=/code
##ENV FLASK_APP app.py
##ENV FLASK_RUN_HOST 0.0.0.0
#EXPOSE 5000
#CMD ["python", "app.py"]

FROM python:3.7-alpine
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .
EXPOSE 5050
CMD [ "python3", "-m" , "flask", "run", "-p 5050","-h 0.0.0.0"]

#CMD ["python", "app.py"]