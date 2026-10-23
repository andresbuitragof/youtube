import re, numpy as np
from vad import load, env
txt=open('/mnt/project-files/videos/02-subir-puntaje/locucion.md',encoding='utf-8').read()
scenes={}
for m in re.finditer(r'### e0(\d)\. [^\n]*\n(.*?)(?=\n### |\n---)',txt,re.S):
    scenes[int(m.group(1))]=m.group(2).strip().replace('\n',' ')
out=[];
for i in range(1,9):
    x=load(f'clean/e0{i}.wav'); d=env(x); thr=max(-45,np.percentile(d,95)-30); sp=d>thr
    # segmentos de voz con cierre de huecos <0.16s
    segs=[];s=None
    for k,v in enumerate(list(sp)+[False]):
        if v and s is None:s=k
        if not v and s is not None:segs.append([s*.02,k*.02]);s=None
    merged=[segs[0]]
    for a,b in segs[1:]:
        if a-merged[-1][1]<0.16: merged[-1][1]=b
        else: merged.append([a,b])
    merged=[m for m in merged if m[1]-m[0]>0.12]
    # descarta ruido inicial aislado (>1s de silencio tras un tramo <0.5s)
    while len(merged)>1 and merged[0][1]-merged[0][0]<0.5 and merged[1][0]-merged[0][1]>1.0:
        print(f'  e0{i}: descarto ruido inicial {merged[0]}'); merged.pop(0)
    # eje de voz
    cum=0;ax=[]
    for a,b in merged: ax.append((a,b,cum)); cum+=b-a
    S=cum
    gaps=[ax[k][2]+ (ax[k][1]-ax[k][0]) for k in range(len(ax)-1)]  # posición en eje de voz
    # frases
    toks=scenes[i].split()
    phr=[[]]
    for w in toks:
        phr[-1].append(w)
        if re.search(r'[.,:;?!”"]$',w): phr.append([])
    phr=[p for p in phr if p]
    L=[sum(len(w)+1 for w in p) for p in phr]; T=sum(L)
    bnd=[sum(L[:k+1])/T*S for k in range(len(phr)-1)]
    # DP monótono
    P=0.7; n=len(bnd); m=len(gaps)
    INF=1e9; D=np.full((n+1,m+1),INF); B={}
    D[0,:]=0
    for a in range(1,n+1):
        for b in range(0,m+1):
            # boundary a sin gap
            best=D[a-1,b]+P; arg=('skip',b)
            for c in range(1,b+1):
                v=D[a-1,c-1]+abs(bnd[a-1]-gaps[c-1])
                if v<best: best=v;arg=('m',c-1)
            D[a,b]=best;B[(a,b)]=arg
    # reconstruir
    a,b=n,m; match={}
    while a>0:
        t,c=B[(a,b)]
        if t=='m': match[a-1]=c; b=c
        a-=1
    # anclas en eje de voz
    anch=[0.0]; wi=[0]
    cw=0
    for k in range(n):
        cw+=len(phr[k])
        if k in match: anch.append(gaps[match[k]]); wi.append(cw)
    anch.append(S); wi.append(len(toks))
    # tiempos por palabra
    flat=[w for p in phr for w in p]; sp_t=[]
    for k in range(len(anch)-1):
        ws=flat[wi[k]:wi[k+1]]; cl=[len(w)+1 for w in ws]; tot=sum(cl); c0=0
        for w,c in zip(ws,cl):
            sp_t.append((anch[k]+c0/tot*(anch[k+1]-anch[k]), anch[k]+(c0+c)/tot*(anch[k+1]-anch[k]),w)); c0+=c
    def real(t):
        for a,b,c in ax:
            if t<=c+(b-a)+1e-9: return a+max(0,t-c)
        return ax[-1][1]
    res=[]
    for a,b,w in sp_t:
        ra=real(a+1e-6); rb=real(b-1e-6)
        res.append([ra,max(rb,ra+0.05),w])
    # mezcla AnnualCreditReport punto com
    j=0
    while j<len(res)-2:
        if res[j][2]=='AnnualCreditReport' and res[j+1][2]=='punto':
            res[j]=[res[j][0],res[j+2][1],'AnnualCreditReport.com'+(',' if res[j+2][2].endswith(',') else '')]
            del res[j+1:j+3]
        j+=1
    rate=len(scenes[i])/S
    print(f'e0{i}: voz {S:.1f}s ritmo {rate:.1f} c/s frases {n+1} anclas {len(match)}/{n}')
    for w in res: out.append(f'E0{i}|{w[0]:.3f}|{w[1]:.3f}|{w[2]}')
open('words.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
