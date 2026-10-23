import numpy as np, subprocess, sys
def load(p):
    r=subprocess.run(f'ffmpeg -loglevel error -i {p} -f f32le -ac 1 -ar 16000 -',shell=True,capture_output=True)
    return np.frombuffer(r.stdout,dtype=np.float32)
def env(x,sr=16000,hop=0.02):
    n=int(sr*hop); m=len(x)//n
    r=np.sqrt((x[:m*n].reshape(m,n)**2).mean(1)+1e-12)
    return 20*np.log10(r)
if __name__=='__main__':
    for i in range(1,9):
        x=load(f'clean/e0{i}.wav'); d=env(x)
        thr=max(-45,np.percentile(d,95)-30)
        sp=d>thr
        # gaps
        gaps=[];s=None
        for k,v in enumerate(sp):
            if not v and s is None:s=k
            if v and s is not None:
                if k-s>=8:gaps.append((round(s*.02,2),round(k*.02,2)))
                s=None
        idx=np.where(sp)[0]
        print(i,'thr',round(thr,1),'speech',round(idx[0]*.02,2),round(idx[-1]*.02,2),'dur',len(x)/16000)
        print('  gaps',gaps)
