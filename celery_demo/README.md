## celery: 常用参数
```markdown
main:如果作为__main__运行，则为主模块的名称。用作自动生成的任务名称的前缀
loader:当前加载器实例。
backend:任务结果url；
amqp:AMQP对象或类名，一般不管；
log:日志对象或类名；
set_as_current:将本实例设为全局当前应用
tasks:任务注册表。
broker:使用的默认代理的URL,任务队列；
include:每个worker应该导入的模块列表，以实例创建的模块的目录作为起始路径；
```