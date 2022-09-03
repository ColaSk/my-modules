# my modules

# 简介

> 包含一些实用的小模块, 因为每个模块特别小，因此不想占用一些仓库资源
> 日益增多的小模块


# 功能
## acid_file (持续优化)

> 需要进一步测试

- 文件
  - 重命名
  - 拷贝
  - 删除
- 文件夹
  - 重命名
  - 拷贝
  - 删除

## sqlalchemy_mixin (持续优化)

- mixin
- atomic
- atomic_begin_nested

## image_info (持续优化)

- xmp
  - 针对pyexiv2对xmp信息获取时无法获取问题做了优化
- exif

## nameko_framework(持续优化)

> nameko 框架 构建方法，以及包含的测试模块
> 准确的说nameko_framework 不是一个供大众使用的可插拔框架，仅仅是基于风格自己构建的服务架子, 
> 使得可以专心构建服务而不是将心思用于框架的搭建，你可以将它看成一个没有任何功能但是又什么都包含的
> 一个例子，仅此而已，顺便又解决了nameko本身存在的一些问题以及基于框架本身特性构建的一些有趣的东西

### 文档
- nameko https://nameko.readthedocs.io/en/stable/index.html

### 问题

#### 原生nameko 不会打印错误日志
- 添加了监控相关依赖，源码见 ./common/extensions/ctx_logger.py

#### 统一格式返回信息(包括成功，错误等)
- 将会破坏rpc规范，将会添加相关解决方案，但是将不会作为rpc代替品，是否应用取决于使用者
- 返回格式类似与http response

#### 外部服务基类
- rpc_service_define
- 定义外部服务基类, 后续可进行 rpc proxy 优化

## fastapi_framework(持续优化)

> fastapi 构建方法，或者说这是一个fastapi的demo

## rpc

> python 的一些 rpc 实现

## aio_mqtt(开发中)

> 一个异步的mqtt 客户端, 基于 hbmqtt 封装实现，改善hbmqtt的代码风格与用法

## myredis(开发中)

> 关于redis的一些算法实现与应用, 对redis一些模块的封装，调整redis库的可用性

## celery_framework(持续优化中)

> 关于celery 框架的用法

## elasticsearch_

> 关于elasticsearch的测试使用

### 问题


> 部署时配置文件挂载存在问题（elasticsearch.yml: Device or resource busy），目前不采用挂载可以正常启动
> 需要解决此问题
