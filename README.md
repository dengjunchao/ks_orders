#### 介绍
快手后端订单服务

#### 软件架构
Mongodb+Flask+Gunicorn+Gevent+Nginx

#### 导出依赖 
pip freeze > requirements.txt

#### 安装依赖包
pip install -r requirement.txt

#### 生产模式启动

python manager.py run

#### 数据库订单字段表语义 

注意:需要mongodb创建表,config配置ip

|字段|type(字段类型)|字段语义|
|:---:|:---:|:---:|
|_id           |ObjectId|订单id|
|orders_type   |int32   |订单类型:1.点赞 2.关注3.评论4.播放量 5.评论赞|
|user_id       |str     |用户id|
|user_name     |str     |用户名字|
|photo_name    |str     |视频名字|
|photo_id      |str     |视频id|
|comment_id    |str     |评论赞id|
|comment_row   |int32   |说说/条|
|orders_date   |int32   |订单时间|
|start_number  |int32   |开始数量|
|now_number    |int32   |当前计数（当前刷个数）|
|order_state   |int32   |订单描述（0.未开始 1.进行中 2.已完成）|
|work_status   |int32   |工作状态(后台使用)|
|sign          |int32   |退单状态 1.正常 2.退单 3.操作完成 4.异常|
|robots_number |int32   |机器人|
|orders_counts |int32   |订单数量|


