# face-compare
人脸比对服务  
<br>
基于 face_recognition ，使用 MongoDB 记录比对日志（不记录日志时可不使用 DB）  
> 由于人像隐私的问题，该项目不存储用户的人脸数据，若用户已授权存储，则只需新建一个人像表即可


## 启动
服务相关的配置在 `config.py` 中，可以设置启动端口、数据库和识别阀值等

```bash
# 启动服务
$ python3 app.py
```

## 测试使用
启动服务后， `/test` 目录中的 `demo.html` 可以测试比对 api  

> 注：  
> 1. 用于测试的比对图片需自己提供  
> 2. 修改服务启动端口地址后， demo.html 中的接口地址也要修改


## API
请求地址： 

```
POST /user/face/compare
```


请求参数：

| 字段 | 必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| origin | 是 | String | 调用来源（该项目若用来当公共服务，需辨别请求来源，若不区分则随意赋值） |
| imgData1 | 是 | String | 图片 base64 编码 |
| imgData2 | 是 | String | 图片 base64 编码 |


返回示例：

```js

// 比对成功
{
  "code": 2000,
  "msg": "比对成功",
  "recognition_result": 1,  // 0-不匹配；1-匹配。（可配合 face_distance 的值一起判断结果）
  "face_distance": 0.36,  // 数值越小，匹配度越高
}


// 比对失败-不匹配
{
  "code": 5002,
  "msg": "比对失败，tolerance 为0.5", // tolerance 为系统设置的用于判断结果的阀值，详见配置文件
  "recognition_result": 0,
  "face_distance": 0.55
}


// 比对失败-未检测到人像
{
  "code": 5005,
  "msg": "未识别图像2中的人像"
}


// 比对失败-图片中有多个人像
{
  "code": 5007,
  "msg": "图像1中的人像过多"
}

// 比对失败-图像解析失败
{
  "code": 5009,
  "msg": "图像1解析失败"
}

```
