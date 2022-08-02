FROM python:3.6

RUN mkdir /service
COPY protobufs /service/protobufs
COPY recommendations /service/recommendations
WORKDIR /service/recommendations

RUN python3 -m pip install --upgrade pip
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
RUN python3 -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

RUN chmod a+x boot.sh

EXPOSE 50051
ENTRYPOINT ["./boot.sh"]