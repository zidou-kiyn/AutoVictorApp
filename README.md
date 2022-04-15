# AutoVictorApp

1. 主程序:VictorApp.py(运行它即可)

2. 用途:

   自动化完成维词打卡 支持的题目类型有如下

   1. 拼写
   2. 英译汉
   3. 汉译英
   4. 构词法拼词
   5. 其余类型除却听音识词均以随机试错选择 自行订正

3. 环境:

   1. python 3.x (需安装模块pip install appium-python-client)
   2. appium server
   3. 雷电模拟器(非必要 但此程序以模拟器为蓝本设计)
   4. jdk
   5. androidsdk

4. 使用方法:

   1. 百度随便找一篇python配置appium的教程即可
   2. 配置完后打开appium server 和模拟器(需用androidsdk内的adb.exe替换目录下的adb.exe)
   3. 配置appium的路径 即edit 需要添加JAVA_HOME ANDROID_HOME(以上均可以百度 此处不过多解释)
   4. 点击appium的start server
   5. 运行VictorApp.py 等待运行 