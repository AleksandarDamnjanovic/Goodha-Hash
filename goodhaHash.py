import math
import string

class GoodhaHash:

    @staticmethod
    def hash(input):

        if isinstance(input, int):
            input= hex(input)
            input=input[2:len(input)]

        if isinstance(input,str):
            input= input.encode().hex()

        if isinstance(input, bytes):
            input= input.hex()

        if isinstance(input, float):
            input= str(input).encode().hex()

        if len(input)<256:
            value= GoodhaHash._spread(input)
        else:
            value= GoodhaHash._cut(input)
            value= GoodhaHash._spread(value)

        value= GoodhaHash._root(value)
        value= GoodhaHash._shift(value)
        value= GoodhaHash._cut(value)
        value= GoodhaHash._spread(value)
        value= GoodhaHash._shift(value)
        value= GoodhaHash._cut(value)

        return '0x'+value

    @staticmethod
    def _spread(input):
        count=0
        r=''
        if input=='':
            for i in range(256):
                res=i & 0xff
                res= hex(res)
                r+=res[2:]
        else:
            for i in range(256):
                e=input[count]
                count+=1
                if count>len(input)-1:
                    count=0

                e=e.encode().hex()
                r+=e

        return r

    @staticmethod
    def _shift(input):
        ret=''
        count=1
        for i in range(0,len(input),2):
            if(i!= len(input)-1):
                e=input[i:i+2]
                e=int(e,16)
                e=e<<count
                count+=1
                if(count==5):
                    count=0
                ret+=hex(e)[2:]
        return ret

    @staticmethod
    def _cut(input):
        ret=''
        count=0
        row=[0x00]*64
        for i in range(0,len(input),2):
            e=input[i:i+2]
            e=int(e,16)
            e= e & 0xff
            if count % 7==0:
                row[count]=row[count]^e
            elif count % 5==0:
                row[count]=row[count]+e
            elif count % 3==0:
                row[count]=row[count]*e
            else:
                row[count]=row[count]+(e<<i%7)
            count+=1
            if count==64:
                count=0

        for i in range(64):
            e= row[i]
            e= e & 0xff

            if e==0x00:
                e='0x00'
            else:
                e=hex(e)

            e=e[2:]

            if(len(e)==1):
                e='0'+e

            ret+=e

        return ret

    @staticmethod
    def _root(input):
        l=[]
        for i in range(0, len(input), 8):
            e= input[i:i+8]
            e=int(e,16)
            r=math.sqrt(e)
            f=int(e)
            p=r-f
            p=p*100000000000
            e=e*f
            e=e^int(p)
            e=hex(e)
            e=e.replace("-",'')
            e=e[2:]
            l.append(e)

        ret= l[15]+l[13]+l[11]+l[9]+l[7]+l[5]+l[3]+l[1]+l[14]+l[12]+l[10]+l[8]+l[6]+l[0]+l[2]+l[4]
        return ret