import numpy as np
import tushare as ts
import matplotlib.pyplot as plt
import pandas as pd
#from sklearn import linear_model

def create(a,n=10,type=1):
    x=len(a)
    v=np.zeros((x-n+1,n),float)
    for i in range(x-n+1):
        if type==1:
           v[i]=a[x-n-i:x-i].values
        else:
           v[i]=a[i:i+n].values[::-1]
    return v


def strategy(x):
    n=len(x)
    t1=np.corrcoef(np.arange(n),x)
    t2=np.corrcoef(np.arange(5),x[n-5:n])
    if (t1[0][1]>0.5)&(t2[0][1]>0.5):
        return 1
    else:
        if(t2[0][1]<-0.5):
          return -1
        else:
          return 0

def strategy2(x):
    if (x[4]>x[3])&(x[3]>x[2])&(x[2]>x[1])&(x[1]>x[0])&(x[5]>x[4]):
        return 1
    else:
        if(x[4]>x[5])&(x[3]>x[4])&(x[2]>x[3]):
          return -1
        else:
          return 0
		  
def strategylist(v):
    n,m=v.shape
    b=np.zeros((n,1))
    a=np.zeros((n,1))
    for i in range(n):
      b[i]=strategy(v[i])
    b=b[::-1]
    for i in range(n):
      if(i==0)&(b[i]==1):
          a[i]=1
      else:
          if(b[i]==1):
              a[i]=1
          if(b[i]==-1):
              a[i]=0
          if(b[i]==0):
              a[i]=a[i-1]
    return a,b
    

def teststrategy(code,bdate,edate):
    data=ts.get_hist_data(code,start=bdate,end=edate)
    print "Code:"+code
    print "Start Date:"+bdate
    print "End Date"+edate
    print "Strategy:"
    v=create(data['close'],n=6,type=2)
    n,m=v.shape
    x=pd.DataFrame()
    x['date']=data.index[0:n].values[::-1]
    x['close']=data['close'][0:n].values[::-1]
    x['keep'],x['action']=strategylist(v)
    x.to_csv("F:\\Github\\quant\\test.csv")
    
              

teststrategy('000001','2015-12-01','2016-06-01')

#data=ts.get_hist_data('000001')
#print data.head()