import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import math


#xmin=2
#xmax=3.82
#h=0.13
#tmax=0.14
#tmin=0.02
#T=0.01
#lam=1
#user_data={'u0_data':"3**(x/2)+x",'ft_data':'(18*t)**2+4.87','zt_data':'12*math.cos(6*t)'}


def solve( xmin,xmax,h,tmin, tmax,T,lam,user_data):
    t_list = []
    x_list = []
    f_list = []
    z_list = []
    u0_list = []
    a_list = [0]
    nt=int((tmax-tmin)/T)
    nx=int((xmax-xmin)/h)

    def u0(x):
        return eval(user_data['u0_data'])
    def ft(t):
        return eval(user_data['ft_data'])
    def zt(t):
        return eval(user_data['zt_data'])

    A=lam/h**2
    B=2*lam/h**2+1/T
    C=A
    F=1/T

    solve=np.full((int(nx+2),int(nt+1)), 0 )
    koef=np.full((int(nx+1),int(nt+1)), 0 )
    for i in range(nt+1):
        t_list.append(tmin + T * i)
        t=t_list[i]
        f_list.append(ft(t))
        z_list.append(zt(t))

    for j in range(nx + 2):
        x_list.append(xmin+h*j)
        x=x_list[j]
        u0_list.append(u0(x))

    df1=pd.DataFrame(solve,index=x_list,columns=t_list)
    kdf=pd.DataFrame(koef,index=x_list[0:-1],columns=t_list)
    df1.iloc[0]=f_list
    df1.iloc[-1]=z_list
    df1[t_list[0]]=u0_list


    f_list[0]=0
    kdf.iloc[0]=f_list
    for s in range(1,nx+1):
        a_list.append(A/(B-C*a_list[s-1]))
    kdf[t_list[0]]=a_list

    for y in range(1,nt+1):
        b_list = [f_list[y]]
        add_list=[z_list[y]]
        for q in range(nx):
            b=(C*b_list[q]+F*df1.iloc[q+1][t_list[y-1]])/(B-C*kdf.iloc[q][t_list[0]])
            b_list.append(b)
        kdf[t_list[y]]=b_list
        for r in range(nx+1,1,-1):
            u=add_list[nx+1-r]*kdf.iloc[r-1][t_list[0]]+kdf.iloc[r-1][t_list[y]]
            add_list.append(u)
        add_list.append(f_list[y])
        add_list.reverse()
        df1[t_list[y]]=add_list
    df1=np.round(df1,decimals=3)
    return df1

#a=solve(xmin,xmax,h,tmin, tmax,T,lam)
#print(a.to_string())
#a.to_excel('solution.xlsx', sheet_name='Лист1')

def temp_map(a):
    figure = ff.create_annotated_heatmap(
        z=a.values,
        x=list(a.columns),
        y=list(a.index)[::-1],
        annotation_text=a.values,
        showscale=True)
    return figure

#fig=temp_map(a)
#fig.show()

def surface(a):
    x = list(a.columns)
    y = list(a.index)[::-1]
    z = a.values

    surf = go.Figure(data=[go.Surface(x=x, y=y, z=z)])
    return surf

#sur=surface(a)
#sur.show()