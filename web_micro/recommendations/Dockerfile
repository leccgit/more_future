FROM python:3.6

RUN mkdir /service
COPY protobufs /service/protobufs
COPY recommendations /service/recommendations
WORKDIR /service/recommendations

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
RUN python3 -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

EXPOSE 50051
ENTRYPOINT [ "python", "recommendations.py" ]
# docker build . -f recommendations/Dockerfile -t recommendations