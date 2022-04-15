from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey

class AppiumAndroidApp(object):
    """ 父类  抽象所有app """
    def __init__(self,platformName,platformVersion,deviceName,appPackage,appActivity,unicodeKeyboard,
                 resetKeyboard,noReset,newCommandTimeout,automationName):
        # 初始化设备信息
        self.desired_caps = {
            'platformName': platformName,  # 被测手机是安卓
            'platformVersion': platformVersion,  # 手机安卓版本
            'deviceName': deviceName,  # 设备名，安卓手机可以随意填写
            'appPackage': appPackage,  # 启动APP Package名称
            'appActivity': appActivity,  # 启动Activity名称
            'unicodeKeyboard': unicodeKeyboard,  # 使用自带输入法，输入中文时填True
            'resetKeyboard': resetKeyboard,  # 执行完程序恢复原来输入法
            'noReset': noReset,  # 不要重置App
            'newCommandTimeout': newCommandTimeout,
            'automationName': automationName
        }
        # 连接Appium Server，初始化自动化环境
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        # 缺省等待
        self.driver.implicitly_wait(5)

    def findElement(self,mode,feature):
        """ 找元素 """
        return self.driver.find_element(mode,feature)

    def findElements(self,mode,feature):
        """找所有元素"""
        return self.driver.find_elements(mode,feature)

    def getText(self,mode,feature):
        """ 返回文本 """
        return self.findElement(mode,feature).text

    def getTexts(self,mode,feature):
        """ 返回文本列表 """
        textList = []
        for i in self.findElements(mode,feature):
            textList.append(i.text)
        # print(textList)
        return textList

    def clickElement(self,mode,feature):
        """ 点击元素 """
        return self.findElement(mode,feature).click()

    def checkElementExist(self,mode,feature):
        """ 使用findElements 判断元素存不存在"""
        if self.findElements(mode,feature):
            return True
        else:
            return False