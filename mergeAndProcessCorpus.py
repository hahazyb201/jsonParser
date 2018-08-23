import os

print('Now start merging documents!')

statsPath='./webPages/'
fileList=os.listdir(statsPath)
print(fileList)
visitedUrl=set()
fw=open('./mergedCorpus','w')
jump=0
for i in range(0,len(fileList)):
    path=os.path.join(statsPath,fileList[i])
    if os.path.isfile(path):
        fr=open(path,'r')
        r=fr.readline()
        while r!='':
            if r=='\n' or r=='\r' or r=='\n\r' or r=='\r\n':
                r=fr.readline()
                continue
            if r[:4]=='http':
                if r.lower() in visitedUrl:
                    jump=1
                else:
                    jump=0
                    visitedUrl.add(r.lower())
                r=fr.readline()
                continue
            if r[:4]=='^^^^':
                r=fr.readline()
                continue
            if jump==0:
                fw.write(r+'\n')
            r=fr.readline()
        fr.close()
        print('finished doc %s'%i)


fw.close()
