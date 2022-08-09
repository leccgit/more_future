FROM python:3.6

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY marketplace/ /service/marketplace/
WORKDIR /service/marketplace
RUN python -m pip install --upgrade pip
RUN python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

RUN chmod a+x boot.sh

EXPOSE 5050
# boot.sh 该处的运行可能存在问题，比如提示文件未找到
ENTRYPOINT ["./boot.sh"]