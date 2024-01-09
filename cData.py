import re
class cData:
    def __init__(self) -> None:
        pass
        
    def seperateLine(self,line):
        num = re.search('[1-9][0-9]{2}\s+',line)
        num = num.span()
        return num

    def takePosition(self,regex, text):
        num = re.search(regex, text)
        if num == None: return 0
        else:return num.span()
    
    def sliceString (self,line,start,end):
        return line[start:end]
    
    def defineValuePos(self,line):
        valuePos=self.takePosition('[.]\s*([0-9]\s*){3}[.]',line) 
        return valuePos

    def formatValue(self,line,start,end):
        value=self.sliceString(line,start+1,end)
        value=value.replace(" ","")
        value=value.replace(".","")
        if re.search('[()]',value)!=None:
            value=value.replace('(','')
            value=value.replace(')','')
            return int(value)*-1
        else:
            return int(value)
        
    #hàm xác định nơi bắt đầu giá trị
    def findStart(self,line,endPos):
        for i in range(endPos-1,0,-1):
            if line[i].isnumeric() == True: continue
            else: break
        return i
    #hàm xác định nơi kết thúc giá trị
    def findEnd(self,line, startPos):
        temp = 0
        for i in range(startPos,len(line)):
            if line[i].isnumeric()==True: temp+=1
            if line[i]==" ":continue
            if line[i]==".": temp = 0
            if temp==4: break
        return i