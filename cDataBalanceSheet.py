import re
from cData import cData
#cấu trúc chung: mã số - đầu kỳ - cuối kỳ
class cDataBalanceSheet(cData):
    def __init__(self,format) -> None:
        self.dataLine=''
        self.accountNum=''
        self.openingValue=0
        self.closingValue=0
        self.belongTo=''
        self.isAccurate=False
        self.checkError=False
        self.Error=''
        self.format=format
    #hàm phụ
    def getDataLine(self,rawData):
        self.dataLine=rawData
        return self
    #các hàm chính
    def getNumAccount(self):
        numPos=self.takePosition('[1-4]\s*([0-9]\s*){2}([a-z]{1})*\s+',self.dataLine)
        self.accountNum=self.sliceString(self.dataLine,numPos[0],numPos[1])
        self.accountNum=self.accountNum.replace(" ",'')
        self.dataLine=self.sliceString(self.dataLine,0,numPos[0])+" "+self.sliceString(self.dataLine,numPos[1],len(self.dataLine))
        return self
    def getValue(self):
        #value 1
        valuePos = self.defineValuePos(self.dataLine)
        start= self.findStart(self.dataLine,valuePos[0])
        end=self.findEnd(self.dataLine,valuePos[1])
        if format==True:
            self.openingValue=int(self.formatValue(self.dataLine,start,end))
        else: self.closingValue=int(self.formatValue(self.dataLine,start,end))
        #value 2
        self.dataLine=self.sliceString(self.dataLine,0,start)+" "+self.sliceString(self.dataLine,end,len(self.dataLine))
        valuePos = self.defineValuePos(self.dataLine)
        start= self.findStart(self.dataLine,valuePos[0])
        end=self.findEnd(self.dataLine,valuePos[1])
        if format ==True:
            self.closingValue=int(self.formatValue(self.dataLine,start,end))
        else: self.openingValue=int(self.formatValue(self.dataLine,start,end))
        return self
    
    def getBelong(self):
        if self.accountNum=="440"|"270":return self
        if re.search('[a-z]',self.accountNum)!=None:
            self.belongTo=self.sliceString(self.accountNum,0,3)
        else:
            if int(self.accountNum)%100==0:
                if self.accountNum[0]=="1"|"2":
                    self.belongTo="270"
                else: self.belongTo='440'
            else: 
                if int(self.accountNum)%10==0:
                    self.belongTo=self.accountNum[0]+"00"
                else:
                    self.belongTo=self.accountNum
                    self.belongTo[2]='0'
        return self
    

            
            

