"""Subtítulos karaoke + barra de progreso + audio final -> out/video2.mp4"""
import json, re, subprocess
from pathlib import Path
OUT = Path('out')
tl = json.load(open(OUT / 'timeline.json')); st = json.load(open(OUT / 'starts.json'))
starts, total = st['starts'], st['total']

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f'{h}:{m:02d}:{s:05.2f}'

ass = ['[Script Info]', 'ScriptType: v4.00+', 'PlayResX: 1920', 'PlayResY: 1080', 'WrapStyle: 2', '',
       '[V4+ Styles]',
       'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
       'Style: Cap,Inter,66,&H002EB9F5,&H00FFFFFF,&H00152A1F,&H96000000,1,0,0,0,100,100,0,0,1,5,2,2,120,120,80,1',
       '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
srt = []; n = 0
for k, sc in enumerate(tl):
    base = starts[k]; ws = sc['words']; chunk = []
    def flush(next_start=None):
        global n
        if not chunk: return
        a = base + chunk[0][0]; b = base + chunk[-1][1] + 0.12
        if next_start is not None: b = min(b, base + next_start)
        txt = ''; prev = chunk[0][0]
        for w0, w1, w in chunk:
            d = int(round((w1 - prev) * 100)); prev = w1
            txt += f'{{\\k{max(d,1)}}}{w} '
        ass.append(f'Dialogue: 0,{ts(a)},{ts(b)},Cap,,0,0,0,,{txt.strip()}')
        n += 1
        f = lambda t: f'{int(t//3600):02d}:{int(t%3600//60):02d}:{int(t%60):02d},{int(round((t%1)*1000))%1000:03d}'
        srt.append(f'{n}\n{f(a)} --> {f(b)}\n{" ".join(w for _, _, w in chunk)}\n')
    for j, (w0, w1, w) in enumerate(ws):
        chunk.append((w0, w1, w))
        chars = sum(len(x[2]) + 1 for x in chunk)
        gap = ws[j + 1][0] - w1 if j + 1 < len(ws) else 9
        if chars > 30 or re.search(r'[.,:;?!]$', w) or gap > 0.4:
            flush(ws[j + 1][0] if j + 1 < len(ws) else None); chunk = []
    flush(); chunk = []
(OUT / 'caps.ass').write_text('\n'.join(ass) + '\n', encoding='utf-8')
(OUT / 'video2.srt').write_text('\n'.join(srt), encoding='utf-8')

vf = (f"drawbox=x=0:y=0:w=iw:h=10:color=0x0A3A2A@0.9:t=fill,"
      f"drawbox=x=0:y=0:w='iw*t/{total:.2f}':h=10:color=0xF5B92E:t=fill,"
      f"ass={OUT}/caps.ass")
cmd = (f'ffmpeg -loglevel error -y -i {OUT}/joined.mp4 -i {OUT}/mix.wav -vf "{vf}" -map 0:v -map 1:a '
       f'-c:v libx264 -preset medium -crf 18 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart {OUT}/video2.mp4')
r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print(r.stderr[-2000:] or 'ok')
