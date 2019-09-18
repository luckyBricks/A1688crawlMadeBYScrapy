# 阿里1688商品列表页
* 基于`Scrapy`实现
* `Spider`目录下存放的是对数据`item`的处理逻辑
* 发货地址`address`目前css还未确定，会随页面刷新更改，正在设计
* 所有的数据存入`MySql`中保存
* 中间件`middlewares.py`用于设置ip池、分布式爬虫

Create by Bricks @ 2019