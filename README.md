# RubberStopper

## 框架简介

这个仓库是一个使用python编写的简单的测试框架，提供了对REST API进行测试的基本功能。用于解决前后端分离式架构，服务端接口测试的痛点，可以有效的进行业务逻辑的隔离测试。

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

### 运行

```
python sample.xlsx
```

## 项目文件结构

```
.
├── sample.xlsx 测试case的模板文件
└── testmain.py 测试框架源代码文件
```

## 测试框架的使用说明

### 概念

* Excel的DataSheet表示一个测试用例
* Excel的每行代表了一个测试步骤

### Excel用例模板的单元格功能解释
- A: 测试接口步骤名字
- B: HTTP请求类型：POST，PUT，GET，DELETE，PATCH
- C: HTTP的URL： /test/endpoints
- D: HTTP参数的方式：（PATH，BODY)
  - PATH:代表路径的参数
  - BODY:代表BODY体的JSON格式数据
- E: 参数数据
- F: HTTP请求返回值：200，或者500等
- G: HTTP请求返回值的期待值
- H: HTTP请求返回值中需要获取的值

#### G HTTP请求返回值的期待值的格式
```
{"expect_value":["key1","key2","key3"}
```
验证的返回结果
```
{ 
  "key1": {
            "key2": {
                      "key3": "expect_value"
                      }
            }
}
```

#### H HTTP请求返回值中需要获取的值
```
{"var": ["key1","key2","key3"]
```
var 代表的变量，存储了通过```["key1","key2","key3"]```获取的数据
var 变量会存储在测试环境中，用于下一个步骤需要数据的传递

#### 参数数据

```
{"data": "数据 {{ var }}" }
```
```{{var}}```代表了一个从其他测试步骤中获取的值




