protobufs 生成Python代码
```markdown
python -m grpc_tools.protoc -I ../protobufs --python_out=. \
         --grpc_python_out=. ../protobufs/recommendations.proto

```
- python -m grpc_tools.protoc运行 protobuf 编译器，它将从 protobuf 代码生成 Python 代码
- -I ../protobufs告诉编译器在哪里可以找到您的 protobuf 代码导入的文件。您实际上并没有使用导入功能，但-I仍然需要该标志。
- --python_out=. --grpc_python_out=.告诉编译器在哪里输出 Python 文件。正如您稍后将看到的，它将生成两个文件，如果您愿意，可以使用这些选项将每个文件放在一个单独的目录中
- ../protobufs/recommendations.proto是 protobuf 文件的路径，该文件将用于生成 Python 代码

