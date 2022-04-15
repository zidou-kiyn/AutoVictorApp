
from appium.webdriver.common.appiumby import AppiumBy
from AppiumAndroidApp import AppiumAndroidApp
from SearchResult import SearchResult
import re,time,difflib
from random import randint

class VictorApp(AppiumAndroidApp):
    def __init__(self,platformVersion,
                 platformName = "Android",
                 deviceName = "VictorEnglishAutoTest",
                 appPackage = "com.android.weici.senior.student",
                 appActivity = "com.android.weici.senior.student.ui.SplashActivity",
                 unicodeKeyboard = True,
                 resetKeyboard = True,
                 noReset = True,
                 newCommandTimeout = 6000,
                 automationName = "UiAutomator2"):
        # 继承父类的构造
        super().__init__(platformName,platformVersion,deviceName,
                                               appPackage,appActivity,unicodeKeyboard,
                                               resetKeyboard,noReset,
                                               newCommandTimeout,automationName)
        self.TITLES = {
            1:self.__spellTitle,
            2:self.__englishToChinese,
            345:self.__question,
            7:self.__buildWord,
        }
        self.searcher = SearchResult()
        self.lastType = '' # 用于保存上一次的题目类型
        self.position = 1 # 抓位置 判断用前面的还是后面的
        self.tryError = 0



    def tellTitle(self):
        """ 辨别题型 """
        self.driver.implicitly_wait(0)
        self.position = self.getPosition()

        if (self.lastType != '拼写' and \
                len(self.findElements(AppiumBy.ID,"com.android.weici.senior.student:id/keyboard")) == 1) or \
                (self.lastType == '拼写' and \
                len(self.findElements(AppiumBy.ID,"com.android.weici.senior.student:id/keyboard")) == 2):
            # 上一次是拼写 则应有两个键盘 上一次不是拼写 则要有一个键盘
            print("拼写")
            return 1

        if (self.lastType != '构词法拼词' and \
            len(self.findElements(AppiumBy.ID, 'com.android.weici.senior.student:id/part_word')) == 1) or \
            (self.lastType == '构词法拼词' and \
            len(self.findElements(AppiumBy.ID, 'com.android.weici.senior.student:id/part_word')) == 2):
            # 如果有part_word则是构词法拼词题型
            print("构词法拼词")
            return 7

        if (self.lastType != '英译汉' and \
            len(self.findElements(AppiumBy.ID, 'com.android.weici.senior.student:id/english')) == 1) or \
            (self.lastType == '英译汉' and \
            len(self.findElements(AppiumBy.ID, 'com.android.weici.senior.student:id/english')) == 2):
            # 如果有part_word则是构词法拼词题型
            print("英译汉")
            return 2

        if (self.lastType != '大杂烩' and \
            len(self.findElements(AppiumBy.ID, 'com.android.weici.senior.student:id/question')) == 1) or \
            (self.lastType == '大杂烩' and \
            len(self.findElements(AppiumBy.ID, 'com.android.weici.senior.student:id/question')) == 2):

            print("大杂烩")
            return 345


    def getPosition(self):
        """ 返回该从前面选 还是从后面 现用于构词法"""
        positionTexts = self.getTexts(AppiumBy.ID,'com.android.weici.senior.student:id/position')
        # print(positionTexts)
        if len(positionTexts) == 1:
            return 1
        else:
            if int(positionTexts[0].replace('/','')) > int(positionTexts[1].replace('/','')):
                return 1
            else:
                return -1

    def solveTitle(self,mode):
        # 解决不同题型
        self.TITLES[mode]()

    def getTotal(self):
        """ 获得总题数 """
        title = self.getText(AppiumBy.ID,"com.android.weici.senior.student:id/position")
        result = int(re.search("/(.+)",title, flags=0).groups()[0]) - \
                 int(re.search("(.+)/",title, flags=0).groups()[0]) + 1
        return result

    def __spellTitle(self):
        """ 解决拼写题型 """
        self.lastType = '拼写'

        # if len(noteTexts) == 1:
        #     self.used_noteText = noteTexts[-1]
        #     noteText = self.used_noteText
        # else:
        #     if noteTexts[-1] != self.used_noteText:
        #         self.used_noteText = noteTexts[-1]
        #         noteText = self.used_noteText
        #     else:
        #         self.used_noteText = noteTexts[0]
        #         noteText = self.used_noteText
        if self.position == 1:
            noteText = self.getTexts(AppiumBy.ID, "com.android.weici.senior.student:id/yinbiao")[0]
            mean = self.reSaveChinese(self.getTexts(AppiumBy.ID,"com.android.weici.senior.student:id/chinese")[0])
        else:
            noteText = self.getTexts(AppiumBy.ID, "com.android.weici.senior.student:id/yinbiao")[-1]
            mean = self.reSaveChinese(self.getTexts(AppiumBy.ID, "com.android.weici.senior.student:id/chinese")[-1])
        note_USA = re.search("美\[(.+)\]",noteText, flags=0).groups()[0]
        words = self.searcher.noteSearchWord(note_USA)
        if len(words) == 1:
            word = words[0]
        # print(word)
        else:
            rates = []
            for i in words:
                answerList = self.searcher.getMeanFromWord(i)
                answerMean = ''
                for j in answerList:
                    answerMean = answerMean + j
                answerMean = self.reSaveChinese(answerMean)
                rates.append(self.compareWordsMean(answerMean,mean))
            word = words[rates.index(max(rates))]



        for char in word:
            # self.clickElement(AppiumBy.ID,"com.android.weici.senior.student:id/key_{}".format(char.upper()))
            self.clickElement(AppiumBy.ANDROID_UIAUTOMATOR,
                              'new UiSelector().resourceId("com.android.weici.senior.student:id/key_{}").clickable(true)'.format(char.upper()))
        self.clickElement(AppiumBy.ID,"com.android.weici.senior.student:id/key_to_confirm")
        time.sleep(1)

    def __buildWord(self):
        """ 解决构词法拼词 """
        self.lastType = '构词法拼词'
        # print(self.position)
        # 以下三者原理相同
        if self.position == 1:
            part = re.search("(.+)\..+",self.getTexts(
                AppiumBy.ID,"com.android.weici.senior.student:id/chinese")[0]).groups()[0]
        else:
            part = re.search("(.+)\..+",self.getTexts(
                AppiumBy.ID,"com.android.weici.senior.student:id/chinese")[-1]).groups()[0]
        if part in ['vt', 'vi']:
            part = 'v'

        if self.position == 1:
            part_word = self.getTexts(
                AppiumBy.ID,"com.android.weici.senior.student:id/part_word")[0]
        else:
            part_word = self.getTexts(
                AppiumBy.ID,"com.android.weici.senior.student:id/part_word")[-1]

        if self.position == 1:
            parts = self.getTexts(AppiumBy.ANDROID_UIAUTOMATOR,
                                  'new UiSelector().className("android.widget.TextView").clickable(true)')[:2]
        else:
            parts = self.getTexts(AppiumBy.ANDROID_UIAUTOMATOR,
                                  'new UiSelector().className("android.widget.TextView").clickable(true)')[-2:]

        wholeWord = []

        for testPart in parts:
            wholeWord.append(part_word+testPart)
            wholeWord.append(testPart+part_word)
        # print(wholeWord,part)
        answer = self.searcher.partSearchWord(wholeWord,part).replace(part_word,"")
        # print(answer)
        elements = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                          'new UiSelector().text("{}").clickable(true)'.format(answer))
        if (len(elements)) == 1 or (len(elements) == 2 and self.position == 1):
            elements[0].click()
        elif len(elements) == 2 and self.position == -1:
            elements[-1].click()

        time.sleep(1)

    def __englishToChinese(self):
        """ 解决英译汉 """
        self.lastType = '英译汉'

        if self.position == 1:
            word = self.getTexts(AppiumBy.ID,'com.android.weici.senior.student:id/english')[0]
            choice_A = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.TextView").clickable(true).index(0)')[0]
            choice_B = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.TextView").clickable(true).index(1)')[1] # 那个听力的标志也符合这个
            choice_C = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.TextView").clickable(true).index(2)')[0]
        else:
            word = self.getTexts(AppiumBy.ID,'com.android.weici.senior.student:id/english')[-1]
            choice_A = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.TextView").clickable(true).index(0)')[-1]
            choice_B = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.TextView").clickable(true).index(1)')[-1]
            choice_C = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                        'new UiSelector().className("android.widget.TextView").clickable(true).index(2)')[-1]

        answer = self.searcher.getMeanFromWord(word) # 列表

        button = [choice_A,choice_B,choice_C]
        choices = [choice_A.text,choice_B.text,choice_C.text]

        # print(choices)
        # print(answer)
        # print(app.driver.page_source)
        # input()
        isGet = 0
        # rates = {1:0,2:0,3:0}
        rates = [0,0,0]

        for choice in choices:
            choiceRe = choice.replace(' ','')

            for i in ['A','B','C']:
                if i in choiceRe:
                    choiceRe = choiceRe.replace(i+'.','')
                    break

            if '；' in choiceRe:
                words = choiceRe.split('；')
            else:
                words = [choiceRe]


            # for i in words:
            #     words[words.index(i)] = self.reSaveChinese(i)

            for word in words:
                for answerWord in answer:
                    answerWord = answerWord.replace(' ','')

                    answerWord = self.reSaveChinese(answerWord)
                    # print(word,answerWord)
                    similarRate = self.compareWordsMean(answerWord,word)
                    # print(word,answerWord,similarRate)
                    if similarRate >= 0.85:
                        answer = choice
                        isGet = 1
                        break
                    else:
                        if similarRate > rates[choices.index(choice)]:
                            rates[choices.index(choice)] = similarRate
                            continue
            if isGet == 1:
                break
            # print(words,answer)
        if isGet != 1:
            # print(rates)
            maxRate = max(rates)
            # print(maxRate)
            # print(similarRates.index(maxRate))
            print(rates)
            button[choices.index(choices[rates.index(maxRate)])].click()
        else:
            button[choices.index(answer)].click()

        time.sleep(1)

    def reSaveChinese(self,mean):
        """ 只保留中文 """
        result = ''
        means = re.findall("[\u4e00-\u9fa5]+" ,mean)
        for i in means:
            result = result+i
        return result

    def compareWordsMean(self,word1,word2):
        """ 比较两个汉字的相似度 """
        return difflib.SequenceMatcher(None, word1, word2).quick_ratio()

    def __question(self):
        """ 解决大杂烩 """
        self.lastType = '大杂烩'
        # 获取文本
        if self.position == 1:
            text = self.getTexts(AppiumBy.ID, 'com.android.weici.senior.student:id/question')[0]
            choice_A = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("android.widget.TextView").clickable(true).index(0)')[0]
            choice_B = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("android.widget.TextView").clickable(true).index(1)')[0]
            choice_C = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("android.widget.TextView").clickable(true).index(2)')[0]
        else:
            text = self.getTexts(AppiumBy.ID, 'com.android.weici.senior.student:id/question')[-1]
            choice_A = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("android.widget.TextView").clickable(true).index(0)')[-1]
            choice_B = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("android.widget.TextView").clickable(true).index(1)')[-1]
            choice_C = self.findElements(AppiumBy.ANDROID_UIAUTOMATOR,
                            'new UiSelector().className("android.widget.TextView").clickable(true).index(2)')[-1]


        # 中文文本
        # print(text)
        # print(self.is_chinese(text))
        if self.is_chinese(text):
            print('————汉译英')
            # 中文文本就从选项中获取意思 对照中文选
            if '；' in text:
                texts = text.split('；')
            else:
                texts = [text]

            choices = [choice_A,choice_B,choice_C]
            choiceTexts = [choice_A.text,choice_B.text,choice_C.text]
            means = []
            rates = [0,0,0]
            isGet = 0
            if 'A.' in choiceTexts[0]:
                choiceTexts[0] = choiceTexts[0].replace('A. ','')
                choiceTexts[1] = choiceTexts[1].replace('B. ','')
                choiceTexts[2] = choiceTexts[2].replace('C. ','')
            for i in choiceTexts:
                means.append(self.searcher.getMeanFromWord(i))
            # print(means)
            # input()
            for meanList in means:
                for choiceMean in meanList:
                    choiceMean = self.reSaveChinese(choiceMean)
                    for questionMean in texts:
                        rate = self.compareWordsMean(questionMean,choiceMean)
                        if rate > 0.85:
                            isGet = 1
                            choices[means.index(meanList)].click()
                            break
                        elif rate > rates[means.index(meanList)]:
                            rates[means.index(meanList)] = rate
                            continue
                    if isGet == 1:
                        break
                if isGet == 1:
                    break
            if isGet != 1:
                print(rates)
                choices[rates.index(max(rates))].click()

            time.sleep(1)
        else:
            # input('————其他题型 请自行输入 且输入回车令程序继续')
            print("————语境题 通过试错系统")
            choices = [choice_A, choice_B, choice_C]
            choices[randint(0,2)].click()
            time.sleep(3)

    def is_chinese(self,string):
        """
        检查整个字符串是否包含中文
        :param string: 需要检查的字符串
        :return: bool
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False



app = VictorApp('7')

while True:
        if input("Are you ready?(输入n退出程序)") != 'n':
            for i in range(app.getTotal()):
                while True:
                    try:
                        app.solveTitle(app.tellTitle())
                        break
                    except Exception as e:
                        # 以上捕捉错误的方法十分幼稚 但懒得写了
                        print('程序发生错误 暂停2s继续>>', e)
                        time.sleep(2)
                        continue
            print("程序执行完成 请自行完成订正")
        else:
            break
