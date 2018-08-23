import json
import csv
from multiprocessing import Pool
import os
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self,temp):
        HTMLParser.__init__(self)
        self.text=''
        self.temp=temp
        if self.temp=='india.com':
            self.meetAside=False
        elif self.temp=='rekhta.org':
            self.meetDiv=False
            self.spanCount=0
            self.spanCnt=0
            self.headerOne=False
        elif self.temp=='yogiadityanath.in':
            self.yogiTableCount=0
            self.articleCount=0
            self.yogiContentCount=0
        elif self.temp=='nytimes.com':
            self.nyComment=0
            self.nyBody=0
            self.articlePara=False
        elif self.temp=='raftaar.in':
            self.newsText=0
        else:
            pass
        
    def _attr(self,attrlist, attrname):
        for attr in attrlist:
            if attr[0] == attrname:
                return attr[1]
        return None
    def handle_starttag(self, tag, attrs):
        if self.temp=='india.com':
            if tag=='aside':
                self.meetAside=True
        elif self.temp=='rekhta.org':
            if tag=='div':
                '''
                if self._attr(attrs,'class')=='TextWrapper':
                    self.meetDiv=True
                '''
                if self._attr(attrs,'class')=='c':
                    self.spanCount=1 if self.spanCount==0 else self.spanCount
                else:
                    pass
            elif tag=='p':
                if self._attr(attrs,'data-l')=='1':
                    self.spanCount=2 if self.spanCount==1 else self.spanCount
                elif self._attr(attrs,'class')=='DivLine':
                    self.spanCnt=1 if self.spanCnt==0 else self.spanCnt
                else:
                    pass
            elif tag=='span':
                self.spanCnt=2 if self.spanCnt==1 else self.spanCnt
            '''
            elif tag=='h1':
                self.headerOne=True
            ''' 
        elif self.temp=='yogiadityanath.in':
            if tag=='tr':
                self.yogiTableCount=1 if self.yogiTableCount==0 else self.yogiTableCount
            elif tag=='td':
                self.yogiTableCount=2 if self.yogiTableCount==1 else self.yogiTableCount
            elif tag=='div':
                self.yogiTableCount=3 if self.yogiTableCount==2 else self.yogiTableCount
                self.articleCount=2 if self.articleCount==1 else self.articleCount
                self.yogiContentCount=2 if self.yogiContentCount==1 else self.yogiContentCount
                if self._attr(attrs,'class')=='w_content':
                    self.yogiContentCount=1 if self.yogiContentCount==0 else self.yogiContentCount
            elif tag=='article':
                self.articleCount=1 if self.articleCount==0 else self.articleCount
            elif tag=='p':
                self.yogiContentCount=3 if self.yogiContentCount==2 else self.yogiContentCount
                self.articleCount=3 if self.articleCount==2 else self.articleCount
            else:
                pass
        elif self.temp=='nytimes.com':
            if tag=='div':
                cla=self._attr(attrs,'class')
                cla=str(cla)
                if 'Comment-content' in cla:
                    self.nyComment=1 if self.nyComment==0 else self.nyComment
                elif cla=='css-1h6whtw':
                    self.nyBody=1 if self.nyBody==0 else self.nyBody
                elif cla=='article-paragraph':
                    self.articlePara=True
                else:
                    pass
            elif tag=='p':
                self.nyComment=2 if self.nyComment==1 else self.nyComment
                self.nyBody=2 if self.nyBody==1 else self.nyBody
            else:
                pass
        elif self.temp=='raftaar.in':
            if tag=='div':
                cla=self._attr(attrs,'class')
                cla=str(cla)
                if cla=='news_text':
                    self.newsText=1 if self.newsText==0 else self.newsText
                elif cla=='detail_txt':
                    self.newsText=2 if self.newsText==1 else self.newsText
                else:
                    pass
        else:
            pass
 
    def handle_endtag(self, tag):
        if self.temp=='india.com':
            if tag=='aside':
                self.meetAside=False
        elif self.temp=='rekhta.org':
            if tag=='p':
                self.spanCount=1 if self.spanCount==2 else self.spanCount
                self.spanCnt=0 if self.spanCnt==1 else self.spanCnt
            elif tag=='div':
                self.meetDiv=False
                self.spanCount=0 if self.spanCount==1 else self.spanCount
            #elif tag!='h1':
            #    self.headerOne=False
            elif tag=='span':
                self.spanCnt=1 if self.spanCnt==2 else self.spanCnt
            else:
                pass
        elif self.temp=='yogiadityanath.in':
            if tag=='div':
                self.yogiTableCount=2 if self.yogiTableCount==3 else self.yogiTableCount
                self.articleCount=1 if self.articleCount==2 else self.articleCount
                if self.yogiContentCount==2:
                    self.yogiContentCount=1
                elif self.yogiContentCount==1:
                    self.yogiContentCount=0
                else:
                    pass
            elif tag=='td':
                self.yogiTableCount=1 if self.yogiTableCount==2 else self.yogiTableCount
            elif tag=='tr':
                self.yogiTableCount=0 if self.yogiTableCount==1 else self.yogiTableCount
            elif tag=='p':
                self.articleCount=2 if self.articleCount==3 else self.articleCount
                self.yogiContentCount=2 if self.yogiContentCount==3 else self.yogiContentCount
            elif tag=='article':
                self.articleCount=0 if self.articleCount==1 else self.articleCount
            else:
                pass
        elif self.temp=='nytimes.com':
            if tag=='p':
                self.nyComment=1 if self.nyComment==2 else self.nyComment
                self.nyBody=1 if self.nyBody==2 else self.nyBody
            elif tag=='div':
                self.nyComment=0 if self.nyComment==1 else self.nyComment
                self.nyBody=0 if self.nyBody==1 else self.nyBody
                self.articlePara=False
            else:
                pass
        elif self.temp=='raftaar.in':
            if tag=='div':
                if self.newsText==2:
                    self.newsText=1
                elif self.newsText==1:
                    self.newText=0
                else:
                    pass
        else:
            pass
    
    def handle_data(self, data):
        if self.temp=='india.com':
            if self.meetAside==True and self.lasttag == 'p':
                self.text+=data
        elif self.temp=='rekhta.org':
            '''
            if self.meetDiv==True and self.lasttag == 'p':
                self.text+=data
            '''
            if self.spanCount==2 and self.lasttag=='span':
                self.text=self.text+data if data[-1]==' ' else self.text+data+' '
            #elif self.headerOne==True and self.lasttag=='p' and len(data)>150:
            #    self.text+=data
            elif self.spanCnt==2:
                self.text=self.text+data if data[-1]==' ' else self.text+data+' '
            else:
                pass
        elif self.temp=='yogiadityanath.in':
            '''
            if self.yogiTableCount==3:
                self.text+=data
            '''
            if self.articleCount==3:
                self.text+=data
            elif self.yogiContentCount==3:
                self.text+=data
            else:
                pass
        elif self.temp=='nytimes.com':
            if self.nyComment==2:
                self.text+=data
            elif self.nyBody==2:
                self.text+=data
            elif self.articlePara:
                self.text+=data
            else:
                pass
        elif self.temp=='raftaar.in':
            if self.newsText==2:
                self.text+=data
        else:
            pass

def processOneFileAtATime(f,fw,domWanted,visited,mp):
    r=f.readline()
    print('entered')
    while r!='':
        hj=json.loads(r)
        if 'content' in hj:
            dom=hj['domain']
            lowerUrl=hj['url'].lower()
            if dom==domWanted and lowerUrl not in visited:
                visited.add(lowerUrl)
                mp.text=''
                try:
                    mp.feed(hj['content'])
                except:
                    fer=open('./errorM','w')
                    fer.write(hj['content'])
                    fer.close()
                    print('errorrrrrrrrrrrrrrrrr!!!!!!!')
                print('text: '+mp.text)
                fw.write(lowerUrl+'\n')
                fw.flush()
                fw.write(mp.text+'\n')
                fw.flush()
                fw.write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'+'\n')
                fw.flush()
        r=f.readline()        


def thatProcess(id,path,domw):
    print('Running process %s, pid is %s' %(id,os.getpid()))
    mp=MyHTMLParser(domw)
    print('mp%s created'%id)
    fw=open('./webPages/webText%s'%id,'w')
    print('lalala')
    path=str(path)
    if os.system('zstd -d '+path)==0:
        path=path[:-5]
    else:
        os.system('rm '+path[:-5])
        return
    f=open(path,'r')
    visited=set()
    processOneFileAtATime(f,fw,domw,visited,mp)
    fw.close()
    f.close()
    os.system('rm '+path)
    print('Finished process %s, pid  %s' %(id,os.getpid()))



dataset='./'
fileList=os.listdir(dataset)
p=Pool(8)
domw=input('Input the domain name: ')

for i in range(0,len(fileList)):
    print(i)
    path=os.path.join(dataset,fileList[i])
    print(path)
    if os.path.isfile(path) and 'zstd' in str(path):
        p.apply_async(thatProcess,args=(i,path,domw))

p.close()
p.join()
'''
for i in range(0,len(fileList)):
    print(i)
    path=os.path.join(dataset,fileList[i])
    print(path)
    if os.path.isfile(path):
        thatProcess(i,os.path.join(dataset,fileList[i]),domw)
'''
print('All subprocess done.')
