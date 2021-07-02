# SimpleCRM
一个简单的crm。  
# 描述及功能
- 这是一个简易的crm
- 使用redis存放sesseion
- 顾客增删改查
- 员工增删改查
- 不同的员工有不同的权限
- 不同的权限可以访问不同的页面
- 老板可以查看各个员工的操作信息，并分级别提示

# 展示

![主页](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625220729254.png)  ![不同的职员看到的不一样](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625221097996.png)
![账单管理页面](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625220930266.png)

![增加一个新的顾客](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625220990894.png)
![删除操作](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625221047470.png)

![可以查看那些员工干了什么事](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625221165705.png)

![客户管理页面](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625221237034.png)

![没有权限访问时](https://gitee.com/lczmx/Note/raw/master/pictures/README.md/1625221496144.png)


# 使用
1. 下载下来  
2. 安装redis
3. 使用命令：`pip install -r requirements.txt`安装依赖

# 注意事项
1. admin的账户密码：
   - 账户：lczmx
   - 密码：123456
2. 职员的账户密码
   - 职员1：lczmx@foxmail.com （权限最高）
   - 职员2：hesheng@qq.com
   - 职员3：abc@qq.com
   - 密码都为123456
   