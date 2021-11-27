from goodhaHash import GoodhaHash as gh

f=open('./goodhaHash.py','rb')
content= f.read()
f.close()

nounce=0
result= gh.hash('base value '+str(nounce))
temp=result

while result.startswith("0x000")!= True:
    nounce+=1
    result= gh.hash(nounce)
    if result==temp:
        print("Error: Hash identical")
        break
    print(f'{nounce}: {result}')
    temp=result

print(f'{len(result)}: {result}')