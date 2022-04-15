
import json,os

class SearchResult():
    def __init__(self):
        with open('Data/fb_word_detail.json', 'r', encoding='utf-8') as self.f:
            self.DATA = json.loads(self.f.read())
        if not os.path.exists('Data/WordCorresponding.json'):
            with open("Data/WordCorresponding.json",'w',encoding='utf-8') as self.f:
                self.WordCorresponding = self.generateWordCorresponding()
                self.f.write(json.dumps(self.WordCorresponding,ensure_ascii=False,indent=4))
        else:
            with open("Data/WordCorresponding.json", 'r', encoding='utf-8') as self.f:
                self.WordCorresponding = json.loads(self.f.read())


    def generateWordCorresponding(self):
        """创建单词 音标 词性 意思列表"""
        self.words = []
        self.word_notes = []
        self.word_parts = []
        self.word_means = [] # 意思过多 用列表作为元素
        for word in self.DATA:
            wordDetail = word
            wordWord = wordDetail['word'] # 单词
            wordNote_USA = wordDetail['usa_phonetic_symbols'] # 美音标
            wordPart = wordDetail['part_of_speech'] # 词性
            if wordPart in ['vt','vi']:
                wordPart = 'v'

            wordMean = []
            for mean in wordDetail['gy_paraphrase']:
                wordMean.append(mean['chinese'])

            self.words.append(wordWord)
            self.word_notes.append(wordNote_USA)
            self.word_parts.append(wordPart)
            self.word_means.append(wordMean) # 注意这是列表

            # 判断是否有派生词
            if wordDetail['gy_derivative'] != []:
                # 存在派生词
                for wordDerivative in wordDetail['gy_derivative']:
                    wordWord = wordDerivative['derivative_word']
                    wordNote_USA = wordDerivative['phonogram']
                    wordPart = wordDerivative['part_of_speech']
                    if wordPart in ['vt', 'vi']:
                        wordPart = 'v'

                    wordMean = [wordDerivative['description']]

                    self.words.append(wordWord)
                    self.word_notes.append(wordNote_USA)
                    self.word_parts.append(wordPart)
                    self.word_means.append(wordMean)  # 注意这是列表




        return {"words":self.words,"notes":self.word_notes,"parts":self.word_parts,"means":self.word_means}

    def noteSearchWord(self,note):
        """ 从音标搜找单词 """
        noteIndexList = self.indexListMore(self.WordCorresponding['notes'],note)
        if len(noteIndexList) == 1:
            return [self.WordCorresponding['words'][noteIndexList[0]]]
        else:
            result = []
            for i in noteIndexList:
                result.append(self.WordCorresponding['words'][i])
            return result


    def partSearchWord(self,wholeWord,part):
        """ 从整个单词和词性找单词 """
        for word in wholeWord:
            if word in self.WordCorresponding["words"]:
                if part == self.WordCorresponding["parts"][self.WordCorresponding["words"].index(word)]:
                    return word
            else:
                continue

    def getMeanFromWord(self,word):
        """ 找单词意思 """
        meanList = []
        wordList = self.indexListMore(self.WordCorresponding["words"],word)
        for i in wordList:
            mean = self.WordCorresponding['means'][i]
            for j in mean:
                if '：' in j:
                    j = j.replace('：','')

                if "；" in j:
                    j = j.split('；')
                    for h in j:
                        meanList.append(h)
                else:
                    meanList.append(j)
        return meanList


    def indexListMore(self,List,element):
        """ 返回 下标 """
        return [i for i, x in enumerate(List) if x == element]

# test = SearchResult()
# # # # print(test.noteSearchWord("'toʊkən"))
# print(test.partSearchWord(['brightate', 'atebright', 'brighten', 'enbright'],"vt"))
# print(test.getMeanFromWord('for example'))
# 只要中文 明天用re弄
