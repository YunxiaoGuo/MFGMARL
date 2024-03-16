import matplotlib.pyplot as plt
import pickle
import matplotlib.path as mpath
import matplotlib.patches as patches 
from svgpath2mpl import parse_path
import xml.etree.ElementTree as etree 
from six import StringIO 
import numpy as np
import PIL
import mpl_toolkits.mplot3d.art3d as art3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pyplot import MultipleLocator
with open(r"C:\Users\Surprise\Desktop\MFGMARL\envv\test_data.pkl", "rb") as file:
    loaded_list = pickle.load(file)
color=['#DF6B66','#FE867F','r','#FFF6F5','#96B253','#00ADDB','#00D6DC','#75FAC8','#00BAFF','#C4F0FF']
#marker=['o','^','s','p','P','*','X','D','v','x']

plt.rcParams['font.family']='Times New Roman'
plt.rcParams['font.size']=15
time_len=len(loaded_list)
##处理icon
def rot(verts, az):
    #顺时针旋转
    rad = az / 180 * np.pi
    verts = np.array(verts)
    rotMat = np.array([[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]])
    transVerts = verts.dot(rotMat)
    return transVerts
def svg2path(svg_rda):
    # svg_rda = "./rad_icon.svg"
    tree = etree.parse(svg_rda)
    root = tree.getroot()
    path_elems = root.findall('.//{http://www.w3.org/2000/svg}path')
    paths = [parse_path(elem.attrib['d']) for elem in path_elems]
 
    verts = paths[0].vertices
    codes = paths[0].codes
    for i in range(1, len(paths)):
        verts = np.concatenate([verts, paths[i].vertices])*100
        codes = np.concatenate([codes, paths[i].codes])
 
    verts = rot(verts, 270)
    verts = np.fliplr(verts)  # 水平翻转，镜像
    icon = mpath.Path(vertices=verts, codes=codes)
    return icon
rda_icon = svg2path(r'C:\Users\Surprise\Desktop\MFGMARL\aircraft_svg\blue.svg')
xm=np.mean(rda_icon.vertices[:,0])
ym=np.mean(rda_icon.vertices[:,1])

##处理数据
rx=[]
ry=[]
rz=[]
bx=[]
by=[]
bz=[]
Pr,Pb=[[],[],[],[],[]],[[],[],[],[],[]]


for i in range(time_len):#各无人机按时间戳的轨迹
    fig=plt.figure()
    ax = fig.add_axes(Axes3D(fig)) 
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
        dx=xr[-1]-xm
        dy=yr[-1]-ym
        ddx=xb[-1]-xm
        ddy=yb[-1]-ym
        rda_icon.vertices[:,0]+=dx
        rda_icon.vertices[:,1]+=dy
        ax.scatter(xr[-1],yr[-1]+3.5,zr[-1],c=color[j],marker=f'${j+1}$',s=25,alpha=1)#红
        patch = patches.PathPatch(rda_icon, facecolor='#C0504D',edgecolor='#C0504D', alpha=0.8)
        ax.add_patch(patch)
        art3d.patch_2d_to_3d(patch, z=zr[-1], zdir="z")
        #ax.scatter(xr[-1],yr[-1]+3.5,zr[-1],c=color[j],marker=f'${j+1}$',s=25,alpha=1)#红
        rda_icon.vertices[:,0]-=dx
        rda_icon.vertices[:,1]-=dy
        rda_icon.vertices[:,0]+=ddx
        rda_icon.vertices[:,1]+=ddy
        patch = patches.PathPatch(rda_icon, facecolor='#4F81BD',edgecolor='#4F81BD', alpha=0.8)
        ax.add_patch(patch)
        art3d.patch_2d_to_3d(patch, z=zb[-1], zdir="z")
        ax.scatter(xb[-1],yb[-1]+3.5,zb[-1],c=color[j+5],marker=f'${j+1}$',s=25,alpha=1)#蓝
        rda_icon.vertices[:,0]-=ddx
        rda_icon.vertices[:,1]-=ddy

    plt.savefig(r'C:\Users\Surprise\Desktop\MFGMARL\figure\figure'+str(i)+'.png',dpi=500)
    plt.cla()
    plt.close("all")
print('绘图完成')

image=[]
for j in range(time_len):
    new=PIL.Image.open(r'C:\Users\Surprise\Desktop\MFGMARL\figure\figure'+str(j)+'.png')
    image.append(new)
image[0].save(r'C:\Users\Surprise\Desktop\MFGMARL\figure\result.gif',append_images=image[1:],save_all=True,duration=5,loop=0,dpi=500)
print('gif生成完毕')






