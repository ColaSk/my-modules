[toc]
# celery services

## 简介
> 本服务通过celery进行任务调度

## 依赖版本
- celery==5.1.2

## 依赖服务

- redis 
- rabbitmq


## docker-compose 配置

```yml
algo:
  container_name: solar_iter_algo
  build: ./solar_iter_celery_algo
  restart: always
  volumes:
    - ./data/media:/docker_media                       # 共享资源数据
    - ./solar_iter_celery_algo:/docker_codes           # work dir
    - ./conf/config.py:/docker_codes/conf/config.py    # config file
  command: /bin/bash ./docker-entrypoint.sh            # 执行
  networks:
    solar_iter_net:
      ipv4_address: "172.27.0.11"
  depends_on:
    - rabbitmq
```

## 版本更新信息

### 1.0

* [x] celery 项目init
* [x] 算法对接
* [x] celery log 配置

### 2.0

* [ ] 监控管理 flower
* [ ] 守护进程代理