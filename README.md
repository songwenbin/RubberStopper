# RubberStopper

## 框架简介

这是一个使用python编写的简单的测试框架，提供了对REST API进行测试的基本功能。用于解决前后端分离式架构，服务端接口测试的痛点，可以有效的进行业务逻辑的隔离测试。

## 测试框架的特点
1. 测试case通过excel编写。
2. 可以在运行时，进行测试步骤的传值。
3. 支持返回结果的子集的验证。

## 安装要求

```
pip install openpyxl
pip install jinja2
pip install jinja2schema
pip install oauthlib.oauth2
pip install requests_oauthlib
pip install request.auth
```

## 项目文件结构

```
.
├── sample.xlsx 测试case的模板文件
└── testmain.py 测试框架源代码文件
```

## 测试框架的模型概念


## 使用说明

### 运行

```
python sample.xlsx
```

