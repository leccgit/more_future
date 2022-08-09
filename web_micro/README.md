
# python微服务: gRPC
微服务是一种复杂的组织系统软件的方式, 特点是无需将所有代码放到一个应用程序中, 将系统分解为独立部署而且相互通信的微服务, 该教程使用gRPC来启动和运行微服务

[全文链接]: <https://realpython.com/python-microservices-grpc/>

## 目标
```markdown
在Python中实现通过 gRPC 相互通信的微服务
实施中间件来监控微服务
单元测试和集成测试您的微服务和中间件
使用Kubernetes将微服务部署到 Python 生产环境
```
业务的扩张, 单体应用代码库的急剧膨胀, 为测试和维护工作带来了巨大的挑战, 各种代码的杂糅调用也让逻辑难以理解, 严重影响了后续的业务升级, 针对这种场景使用微服务进行重构, 貌似是一种不错的选择。

但是, 伴随微服务的增多, 管理和维护的开销也会同等增大, 需要部署多个服务才能提供一份功能, 不同服务之间调用也会导致一些隐藏的bug难以定位和排查, 服务的边界难以界定微服务到底要多小, 是一个难以讨论的话题。

在Python中实现微服务可能会在短期内花费时间和精力，但也能让我们在长期内得到更好地扩展。不过，过早实施微服务可能会减慢我们的速度。

## 注
```markdown
gRPC中使用了 proto协议, 需要提前有所了解
微服务使用docker 进行部署, 对docker也需要有一定的了解 https://docs.docker.com/engine/reference/builder/
```

为什么使用 proto略...
为什么使用 gRPC略....

protobufs 生成Python代码
```markdown
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
         --grpc_python_out=. ../protobufs/recommendations.proto

```
- python -m grpc_tools.protoc运行 protobuf 编译器，它将从 protobuf 代码生成 Python 代码
- -I ../protobufs告诉编译器在哪里可以找到您的 protobuf 代码导入的文件。您实际上并没有使用导入功能，但-I仍然需要该标志。
- --python_out=. --grpc_python_out=.告诉编译器在哪里输出 Python 文件。正如您稍后将看到的，它将生成两个文件，如果您愿意，可以使用这些选项将每个文件放在一个单独的目录中
- ../protobufs/recommendations.proto是 protobuf 文件的路径，该文件将用于生成 Python 代码

