"""Mesure les bords de la face avant du jonc vierge (contenu/lou/jonc-vierge-v3, repère 1024) → tables JONC de theme-lou/assets/lou.js.
Lancer depuis la racine du dépôt : python3 scripts/mesure_jonc.py (les estimations visuelles xs/ht/bs guident la détection)."""
from PIL import Image, ImageFilter; import numpy as np
xs=[130,180,230,280,330,430,530,550,600,650,700,750,800,850,900,950]
ht=[610,628,645,658,666,673,678,677,675,672,666,660,649,635,617,592]
bs=[663,685,707,720,728,737,740,740,738,736,730,723,713,700,683,657]
P=lambda x,t: np.interp(x,xs,t)
res={}
for n in ['argentee','doree','rosee']:
  im=np.asarray(Image.open(f'contenu/lou/jonc-vierge-v3/jonc-vierge-{n}.jpg').convert('L').resize((1024,1024),Image.LANCZOS).filter(ImageFilter.GaussianBlur(1)),float)
  g=np.diff(im,axis=0)
  H=[];B=[]
  for x in range(140,941,10):
    e=int(P(x,ht)); w=g[e-12:e+12,x-2:x+3].mean(1); H.append(e-12+np.argmin(w)+0.5)
    e=int(P(x,bs)); w=g[e-12:e+12,x-2:x+3].mean(1); B.append(e-12+np.argmin(w)+0.5)
  res[n]=(np.array(H),np.array(B))
X=np.arange(140,941,10)
for n,(H,B) in res.items(): print(n,'H',H.astype(int).tolist()); print(n,'B',B.astype(int).tolist())
H=np.mean([res[n][0] for n in res],0); B=np.mean([res[n][1] for n in res],0)
ok=(X>=150)&(X<=890)
ph=np.polyfit(X[ok],H[ok],4); pb=np.polyfit(X[ok],B[ok],4)
print('err H',np.abs(np.polyval(ph,X[ok])-H[ok]).max(),'err B',np.abs(np.polyval(pb,X[ok])-B[ok]).max())
xx=np.arange(100,971,10)
print('haut: ['+','.join(f'{v:.1f}' for v in np.polyval(ph,xx))+'],')
print('bas: ['+','.join(f'{v:.1f}' for v in np.polyval(pb,xx))+']')
print('h centre', np.polyval(pb,535)-np.polyval(ph,535))
