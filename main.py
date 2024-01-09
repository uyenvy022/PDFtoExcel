import re
import openpyxl
import PyPDF2
import os
import sys
from cBalanceSheet import cBalanceSheet
from cDataBalanceSheet import cDataBalanceSheet
def checkLinkValid(filePath):
    if os.path.isfile(filePath)==True:
        if (re.search('.pdf',filePath)!=None):
            return True
        else: return ("Đây không phải file PDF.")
    else: return ("File không tồn tại.")

def getFormat(format):
    if format=="Y": return True
    else:
        if format=="N":return False
        else: return ("Trả lời không hợp lệ.")
    
def createBalanceSheet(filePath,format,start,end):
    balanceSheet = cBalanceSheet(filePath,format,start,end)
    balanceSheet.getTxt()
    balanceSheet = balanceSheet.getDataList()
    return balanceSheet
def checkValidFileName(fileName):
    fileLocation ='./'+fileName+'.xlsx'
    if os.path.exists(fileLocation)==True:
        return False
    else: return True
def tryParseInt (temp):
    try:
        temp = int(temp) 
        return True
    except ValueError:
        return False
#main
while True:
    print("Nhập filepath của PDF cần chuyển")
    filePath = input()
    checkValid=checkLinkValid(filePath)
    if checkValid==True:break
    else: print(checkValid)
# có cần kiểm tra hay không?
while True:
    print("Vui lòng nhập trang bắt đầu của BCĐKT")
    pageStart = input()
    if tryParseInt(pageStart)==True:break
while True:
    print("Vui lòng nhập trang kết thúc của BCĐKT")
    pageEnd = int(input())
    if tryParseInt(pageEnd)==True:break
while True:
    print ("Trong file PDF, nếu thứ tự các cột là Đầu kỳ - Cuối kỳ, chọn Y. Ngược lại, chọn N")
    formatInput=input()
    format = getFormat(formatInput)
    if (type(format)!=str):break
# tạo balance sheet
balanceSheet = createBalanceSheet(filePath,format,pageStart,pageEnd)
for line in balanceSheet.data:
    try:
        line=line.getNumAccount()
        line=line.getValue()
    except: 
        line.checkError = True
        line.Error=sys.exc_info()[0]
        continue
while True:
    print("Vui lòng nhập tên file xuất ra")
    fileName = input()
    if checkValidFileName(fileName)==False:
        print("File đã tồn tại. vui lòng chọn tên khác.")
    else:break
excelPath=balanceSheet.extractToExcel(fileName)
balanceSheet.deleteFile()
print('File Excel đã được tạo.')
