from cDataBalanceSheet import cDataBalanceSheet
import openpyxl
import re
import PyPDF2
import os
class cBalanceSheet:
    def __init__(self,filePath,format,start,end) -> None:
        self.pdfFilePath=filePath
        self.data=[cDataBalanceSheet(format)]
        self.start=start-1
        self.end=end
        #cấu trúc chung: mã số - đầu kỳ trước - cuối kỳ sau
        self.format=format
    
    def getTxt(self):
        with open(self.pdfFilePath, mode='rb') as f:
            txt_output=''
            reader = PyPDF2.PdfFileReader(f)
            for i in range (self.start,self.end):
                page = reader.getPage(i)
                txt_output += page.extract_text()
        with open('temp.txt', 'w+', encoding='utf-8') as file_obj:
            for line in txt_output:
                file_obj.write(line)
    
    def getDataList(self):
        fileTxt=open ("temp.txt", 'r', encoding='utf-8')
        while True:
            line = fileTxt.readline()
            if re.search('([1-4][0-9]{2}\s+)|([1-4][0-9]{2}[a-z])',line)!=None:
                newData=cDataBalanceSheet(self.format)
                if re.search('([0-9]+[.][0-9]{3})',line)!=None:
                    newData = newData.getDataLine(line)
                    self.data.append(newData)    
                else:
                    nextLine=fileTxt.readline()
                    if (re.search('[.]\s*([0-9]\s*){3}[.]',nextLine)!=None):
                        newData=newData.getDataLine(line+nextLine)
                        self.data.append(newData)
            if not line:
                break
        return self
    

    def extractToExcel(self,fileName):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Mã số","Số đầu kỳ","Số cuối kỳ"])
        for i in range(1,len(self.data)):
            ws.append([self.data[i].accountNum,self.data[i].openingValue,self.data[i].closingValue])
        wb.save(fileName+'.xlsx')
    def deleteFile(self):
        os.remove('temp.txt')
