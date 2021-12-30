#*****************************
#Title: Goodha Hash
#Author: Aleksandar Damnjanovic
#Date: 27.11.2021
#Last edit: 30.12.2021
#*****************************

import math
import string
import struct

class GoodhaHash:

    @staticmethod
    def hash(input, type='hex', pack= True):

        if type=='hex':
            input= hex(input)
            input=input[2:len(input)]

        if type=='string':
            input= input.encode().hex()

        if type=='bytes':
            input= input.hex()

        if type=='float':
            input= str(input).encode().hex()

        value=''
        if len(input)<256:
            value= GoodhaHash._spread(input)
        else:
            value= GoodhaHash._cut(input)
            value= GoodhaHash._spread(value)

        value= GoodhaHash._cut(value)
        if len(value)<256:
            value= GoodhaHash._spread(value)
            value= GoodhaHash._cut(value)
        
        value= GoodhaHash._shift(value)
        value= GoodhaHash._mess(value)
        value= GoodhaHash._cut(value)
        value= GoodhaHash._shift(value)

        if pack:
            value= GoodhaHash._pack(value)

        return '0x'+value

    @staticmethod
    def _spread(input):
        r=input
        if input=='':
            for i in range(256):
                res=i & 0xff
                res= hex(res)
                r+=res[2:]
        else:
            for i in range(256-len(input)):
                e='0'
                r=e+r

        return r

    @staticmethod
    def _mess(input):
        d=list()
        for i in range(0,len(input),16):
            d.append(int(input[i:i+16],16))

        if len(d)==7:
            d.append(d[2])

        if len(d)==6:
            d.append(d[3])
            d.append(d[1])   

        for i in range(8):
            d[i]+=d[0]

        for i in range(8):
            d[i]*=d[1]

        for i in range(8):
            d[i]= d[i] - d[2]

        for i in range(8):
            d[i]-=d[4]

        for i in range(8):
            d[i]|=d[5]

        for i in range(8):
            d[i]^=d[6]

        for i in range(8):
            d[i]&=d[7]

        value=''
        for i in range(len(d)):
            vv=hex(d[i])
            value+=vv[2:]

        return value

    @staticmethod
    def _shift(input):
        d=list()
        for i in range(0,len(input),16):
            d.append(int(input[i:i+16],16))

        for i in range(len(d)):
            d[i]=d[i]<<3|5>>d[i]

        value=''
        for i in range(len(d)):
            vv=hex(d[i])
            value+=vv[2:]

        return value    
        

    @staticmethod
    def _cut(input):
        l=list()
        d=[0x0000000000000000]*8
        for i in range(0,len(input),16):
            l.append(input[i:i+16])

        count=0
        for i in range(len(l)):
            d[count]= d[count]+int(l[i],16)
            count+=1
            if count==8:
                count=0
        
        d1=[0]*8
        for i in range(len(d)):
            d1[i]=d[i]<<4|4>>d[i]
        
        for i in range(len(d)):
            d[i]=d[i]^d1[i]
        
        count=0
        for i in range(len(d)):
            d[i]=d[i]<<count|(8-count)>>d[i]
            count+=1

        count=8
        for i in range(len(d1)):
            d1[i]=d1[i]<<count|(8-count)>>d1[i]
            count-=1

        d2=[0]*8
        for i in range(len(d2)):
            d2[i]=d[i]|d1[i]

        for i in range(len(d)):
            vv=(d2[i]*d1[i])^(d2[i]-d1[i])
            d[i]=d[i]^vv

        value=''
        for i in range(len(d)):
            vv=hex(d[i])
            value+=vv[2:]

        return value

    @staticmethod
    def _shift(input):
        ret=''
        count=1
        for i in range(0,len(input),2):
            if(i!= len(input)-1):
                e=input[i:i+2]
                e=int(e,16)
                e=e<<count|(8-count)>>e
                count+=1
                if(count==5):
                    count=0
                ret+=hex(e)[2:]
        return ret

    @staticmethod
    def _pack(input):
        count=0
        while len(input)>128:
            s=input[len(input)-16:]
            input=input[0:len(input)-16]
            s=int(s,16)
            t= input[count*16:(count+1)*16]
            t= int(t, 16)
            t=t^s
            t=hex(t)[2:]
            part1= input[:count*16]
            part2= input[(count+1)*16:]
            input= part1 + t + part2
            count+= 1
            if count==8:
                count=1

        return input