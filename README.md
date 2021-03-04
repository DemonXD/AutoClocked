## 网页自动打卡脚本

### 软件版本

- python == 3.7.7
- APScheduler == 3.6.3
- selenium == 3.141.0
- chrome  88.0.4324.190

### 描述

1. 8:30-8:59 之间执行随机时间生成程序
2. 打卡程序每5秒执行一次
    * 判断打卡时间是否有效
        * 如果有效则打卡
        * 如果无效则不做动作
3. 当8:59分之前没有打卡，则无论如何都执行一次打卡程序进行打卡

- 判断是否打卡：
    - 判断目录中是否有当天的截图


### 安装
* 编辑src/autoclocked.xml
    * id, name, description都是显示在windows服务中的信息
    * env APP_HOME 配置的是项目所在目录
    * executabledirectory 配置的是python.exe 的路径
```Shell
<configuration>
    <id>AutoClocked</id>
    <name>AutoClocked</name>
    <description>this app for auto clocked on Career Web service</description>
    <env name="APP_HOME" value="E:\Programs\Miniconda"/>
    <workingdirectory>%APP_HOME%</workingdirectory>
    <executable>%APP_HOME%\python.exe</executable>
    <arguments>D:\AutoClocked\src\autoClocked.py</arguments>
</configuration> 
```
* 打开`src\autoClocked.py`配置`clocked_url`打卡地址
* install: winsw.exe install src\autoclocked.xml
* uninstall: winsw.exe uninstall src\autoclocked.xml

### 流程描述
一个流程循环：
> 开始      ←
>   ↓              ↑
> 检查是否已打卡 -> 是
>   ↓
> 检查是否可以打卡 -> 否 -> goto start
>   ↓ 是
> 生成打卡时间
>   ↓
> 判断打卡时间是否有效 -> 否 -> goto start
>   ↓
> 打卡 
>   ↓
> 打卡时间置None
>   ↓
> 结束