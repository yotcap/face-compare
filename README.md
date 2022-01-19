# face-compare
人脸比对服务  
<br>
基于 face_recognition ，使用 MongoDB 记录比对日志（不记录日志时可不使用 DB）


## 启动
服务相关的配置在 config.py 中，可以设置启动端口、数据库和识别阀值等

```bash
$ python3 app.py
```

## 测试使用
启动服务后， `/test` 目录中的 `demo.html` 可以测试比对 api  

> 注：  
> 1. 用于测试的比对图片需自己提供  
> 2. 修改服务启动端口地址后， demo.html 中的接口地址也要修改
