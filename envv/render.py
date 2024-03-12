import matplotlib.pyplot as plt
import pickle
import matplotlib.path as mpath
import matplotlib as mpl 
from svgpath2mpl import parse_path
import xml.etree.ElementTree as etree 
from six import StringIO 
import re
import numpy as np
import PIL
with open(r"C:\Users\Surprise\Desktop\MFGMARL\env\test_data.pkl", "rb") as file:
    loaded_list = pickle.load(file)
color=['#8ECFC9','#FFBE7A','#FA7F6F','#82B0D2','#BEB8DC','#E7DAD2','#999999','#2878B5','#C82423','#96C37D']
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
for i in range(time_len):#各无人机按时间戳的轨迹
    fig=plt.figure(figsize=(10,10))
    ax=plt.axes(projection='3d')
    ax.set_title('3d_track')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
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
        ax.scatter(xr,yr,zr,c=color[8],marker=marker[j],label='r'+str(j+1))#红
        ax.scatter(xb,yb,zb,c=color[7],marker=marker[j+5],label='b'+str(j+1))#蓝

        plt.legend(ncol=5)
        
    fig.tight_layout()
    plt.savefig(r'C:\Users\Surprise\Desktop\MFGMARL\figure\figure'+str(i)+'.png')
    plt.cla()
    plt.close("all")
print('绘图完成')

image=[]
for j in range(time_len):
    new=PIL.Image.open(r'C:\Users\Surprise\Desktop\MFGMARL\figure\figure'+str(j)+'.png')
    image.append(new)
image[0].save(r'C:\Users\Surprise\Desktop\MFGMARL\figure\result.gif',append_images=image[1:],save_all=True,duration=5,loop=0)
print('gif生成完毕')






