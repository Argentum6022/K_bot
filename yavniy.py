# Импорты
import numpy as np
import pandas as pd
import math




xmin=2
xmax=3.82
h=0.13
tmax=0.14
tmin=0.02
T=0.01
lam=1

t_list = []
x_list = []
f_list = []
z_list = []
u0_list = []
def u0(x):
    return 3**(x/2)+x
def ft(t):
    return (18*t)**2+4.87
def zt(t):
    return 12*math.cos(6*t)
lam=1
def solve( xmin,xmax,h,tmin, tmax,T,lam):
    nt=int((tmax-tmin)/T)
    nx=int((xmax-xmin)/h)
    solve=np.full((int(nt+1),int(nx+2)), 0 )
    for j in range(nx+2):
        x_list.append(xmin+h*j)
        x=x_list[j]
        u0_list.append(u0(x))
    for i in range(nt + 1):
        t_list.append(tmin + T * i)
        t=t_list[i]
        f_list.append(ft(t))
        z_list.append(zt(t))
    df=pd.DataFrame(solve,index=t_list,columns=x_list)
    df[x_list[0]]=f_list
    df[x_list[-1]]=z_list
    df.iloc[0]=u0_list
    for p in range(nt):
        add_list=[]
        add_list.append(f_list[p + 1])
        for k in range(1,nx+1):
            u=df.iloc[p][x_list[k]]+lam*T*(df.iloc[p][x_list[k+1]]-2*df.iloc[p][x_list[k]]+df.iloc[p][x_list[k-1]])/h**2
            add_list.append(u)
        add_list.append(z_list[p+1])
        df.iloc[p+1]=add_list
    sol=np.round(df,decimals=2)
    return sol
a=solve(xmin,xmax,h,tmin, tmax,T,lam)
print(a)