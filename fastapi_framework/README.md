# fastapi framework

## 简介

- 初始化框架

## 库

- tortoise-orm[aiomysql] - orm
- aerich - 迁移工具
- fastapi - api
- uvicorn - server
- loguru - log
- pytomlpp - confile
- python-jose[cryptography] - jwt
- passlib[bcrypt] - hash password

## 项目初始化

- 初始化配置文件

```shell

cp ./docs/config.example.toml ./config/config.toml
```

- 初始化数据库

```shell

# aerich 的具体用法详情见 https://tortoise-orm.readthedocs.io/en/latest/migration.html#init-db
aerich init-db # 初始化数据库, 已初始化过，因此不再需要
aerich migrate # 更新模型并迁移
aerich upgrade # 更新数据库
```

## tree

```
fastapi_framework/
├── apps
│   ├── admin
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── application.py
│   ├── exceptions
│   │   ├── exception.py
│   │   ├── __init__.py
│   ├── extensions
│   │   ├── depends.py
│   │   ├── __init__.py
│   │   ├── log.py
│   │   ├── requests.py
│   │   ├── response.py
│   │   ├── route.py
│   │   └── tokens.py
│   ├── __init__.py
│   ├── middlewares
│   │   ├── __init__.py
│   │   ├── middleware.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── mixin.py
│   │   ├── models.py
│   ├── modules
│   └── test_api
│       ├── __init__.py
│       ├── urls.py
│       └── views.py
├── config
│   ├── config.toml
│   ├── __init__.py
│   └── setting.py
├── database
│   └── __init__.py
├── Dockerfile
├── docs
│   └── deploy
│       └── config.example.toml
├── migrations
│   └── models
│       ├── 0_20220311143112_init.sql
│       └── 1_20220311173303_update.sql
├── mirrors
│   └── sources.list
├── pyproject.toml
├── README.md
├── requirements.txt
├── test_data
└── utils
    ├── __init__.py
    └── util.py
```
