import matplotlib.pyplot as plt
import pickle
import numpy as np
import PIL
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
with open(r"C:\Users\Surprise\Desktop\MFGMARL\envv\test_data.pkl", "rb") as file:
    loaded_list = pickle.load(file)
color=['#DF6B66','#FE867F','r','#FFF6F5','#96B253','#00ADDB','#00D6DC','#75FAC8','#00BAFF','#C4F0FF']
marker=['o','^','s','p','P','*','X','D','v','x']

plt.rcParams['font.family']='Times New Roman'
plt.rcParams['font.size']=15
time_len=len(loaded_list)
rx=[]
ry=[]
rz=[]
bx=[]
by=[]
bz=[]
Pr,Pb=[[],[],[],[],[]],[[],[],[],[],[]]

flag=0
for i in range(time_len):#各无人机按时间戳的轨迹

    rx.append(loaded_list[i][0][0])
    ry.append(loaded_list[i][1][0])
    rz.append(loaded_list[i][2][0])
    bx.append(loaded_list[i][0][1])
    by.append(loaded_list[i][1][1])
    bz.append(loaded_list[i][2][1])
    for j in range(5):#第j架飞机最新一次的各坐标
        rrx=rx[-1][j]
        rry=ry[-1][j]
        rrz=rz[-1][j]
        bbx=bx[-1][j]
        bby=by[-1][j]
        bbz=bz[-1][j]
        r=[rrx,rry,rrz]
        b=[bbx,bby,bbz]
        Pr[j].append(r)
        Pb[j].append(b)
        xr,yr,zr=[],[],[]
        xb,yb,zb=[],[],[]
        
        for m in range(len(Pr[j])):
            xr.append(Pr[j][m][0])
            yr.append(Pr[j][m][1])
            zr.append(Pr[j][m][2])
        for n in range(len(Pb[j])):
            xb.append(Pb[j][n][0])
            yb.append(Pb[j][n][1])
            zb.append(Pb[j][n][2])
        if i==time_len-1 and flag==0:
            fig=plt.figure()
            ax = fig.add_axes(Axes3D(fig)) 
            ax.set_title('3d_track')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.plot(xr,yr,zr,c='#C0504D',lw=2,label=f'R_{j+1}',linestyle='--')
            ax.plot(xb,yb,zb,c='#4F81BD',lw=2,label=f'B_{j+1}')
            flag=1
        elif i==time_len-1 and flag==1:
            ax.plot(xr,yr,zr,c='#C0504D',lw=2,label=f'R_{j+1}',linestyle='--')
            ax.plot(xb,yb,zb,c='#4F81BD',lw=2,label=f'B_{j+1}')     
plt.legend(ncol=5,prop = {'size':8},loc='best')
fig.savefig(r'C:\Users\Surprise\Desktop\MFGMARL\figure_track\\3d_track.png', dpi=300)