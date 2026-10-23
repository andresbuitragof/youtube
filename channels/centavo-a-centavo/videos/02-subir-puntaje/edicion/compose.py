"""Monta el video 1 a partir de words.txt (E##|ini|fin|palabra), clean/e##.wav y frames/*.png."""
import json, re, subprocess, unicodedata, os
from pathlib import Path

FPS = 30
W, H = 1920, 1080
OUT = Path('out'); OUT.mkdir(exist_ok=True)

def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return re.sub(r'[^a-z0-9 ]', '', ''.join(c for c in s if unicodedata.category(c) != 'Mn'))

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-3000:]); raise SystemExit(cmd)
    return r.stdout

# ---- palabras
words = {}
for line in Path('words.txt').read_text(encoding='utf-8').splitlines():
    p = line.strip().split('|')
    if len(p) < 4 or not p[0].upper().startswith('E'): continue
    words.setdefault(p[0].upper(), []).append([float(p[1]), float(p[2]), p[3].strip()])

# cortes manuales opcionales (tomas repetidas): {"E03": [[ini, fin], ...]} en tiempo original
CUTS = json.loads(Path('cuts.json').read_text()) if Path('cuts.json').exists() else {}

# disparadores: (estado, frase que lo activa)
TRIG = {
 'E01': [(1, 'cuatro que si'), (2, 'tres que te'), (3, 'quedate hasta')],
 'E02': [(1, 'nadie puede'), (2, 'bancos reportan'), (3, 'treinta dias')],
 'E03': [(1, 'treinta y cinco'), (2, 'atrasado'), (3, 'programa el')],
 'E04': [(1, 'limite de mil'), (2, 'por debajo del treinta'), (3, 'por debajo del diez'), (4, 'antes de la fecha')],
 'E05': [(1, 'si hay un'), (2, 'numero cuatro'), (3, 'si no pagan')],
 'E06': [(1, 'primero'), (2, 'lo que si puedes'), (3, 'segundo'), (4, 'paga el saldo')],
 'E07': [(1, 'cada solicitud'), (2, 'una sola'), (3, 'pero varias'), (4, 'pide solo')],
 'E08': [(1, 'paga a tiempo'), (2, 'usa menos'), (3, 'revisa tu'), (4, 'no cierres'), (5, 'borrar el mal'), (6, 'pedir muchas'), (7, 'cuentame'), (8, 'proximo video'), (9, 'suscribete')],
}

def keep_ranges(sc):
    ws = words[sc]
    start = max(0, ws[0][0] - 0.12); end = ws[-1][1] + 0.35
    cuts = sorted(CUTS.get(sc, []))
    # acortar pausas largas entre palabras
    for a, b in zip(ws, ws[1:]):
        gap = b[0] - a[1]
        if gap > 0.55:
            cuts.append([a[1] + 0.22, b[0] - 0.12])
    cuts = sorted(cuts)
    ranges, cur = [], start
    for c0, c1 in cuts:
        if c1 <= cur or c0 >= end: continue
        ranges.append([cur, max(cur, c0)]); cur = c1
    ranges.append([cur, end])
    return [r for r in ranges if r[1] - r[0] > 0.02]

def mapper(ranges):
    def f(t):
        acc = 0
        for a, b in ranges:
            if t < a: return acc
            if t <= b: return acc + t - a
            acc += b - a
        return acc
    return f

timeline = []  # escenas con duración y palabras mapeadas
for sc in sorted(words):
    i = sc[1:]
    rg = keep_ranges(sc); m = mapper(rg)
    filt = ''.join(f"[0]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{k}];" for k, (a, b) in enumerate(rg))
    filt += ''.join(f'[a{k}]' for k in range(len(rg))) + f'concat=n={len(rg)}:v=0:a=1[o]'
    run(f'ffmpeg -loglevel error -y -i clean/e{i.lower()}.wav -filter_complex "{filt}" -map "[o]" -ar 48000 -ac 1 {OUT}/v{i}.wav')
    dur = float(run(f'ffprobe -v error -show_entries format=duration -of csv=p=0 {OUT}/v{i}.wav'))
    cut_words = [(c0, c1) for c0, c1 in CUTS.get(sc, [])]
    mw = [[m(a), m(b), w] for a, b, w in words[sc] if not any(c0 <= (a + b) / 2 <= c1 for c0, c1 in cut_words)]
    # beats
    text = [norm(w) for _, _, w in mw]
    beats = [(0, 0.0)]; pos = 0
    for st, phrase in TRIG.get(sc, []):
        toks = norm(phrase).split()
        for j in range(pos, len(text) - len(toks) + 1):
            if all(text[j + q].startswith(toks[q]) for q in range(len(toks))):
                beats.append((st, max(0.0, mw[j][0] - 0.15))); pos = j + 1; break
        else:
            print('AVISO: no encontré', sc, phrase)
    timeline.append(dict(sc=sc, i=i, dur=dur, words=mw, beats=beats))
    print(sc, f'{dur:.1f}s', 'beats', [(s, round(t, 1)) for s, t in beats])

json.dump(timeline, open(OUT / 'timeline.json', 'w'), ensure_ascii=False, indent=1)

# ---- video por escena: imágenes por beat + zoom lento
XF = 0.35  # duración del cruce entre escenas
for k, sc in enumerate(timeline):
    i = sc['i']; lst = []
    bt = sc['beats'] + [(None, sc['dur'] + (XF if k < len(timeline) - 1 else 0))]
    for (st, t0), (_, t1) in zip(bt, bt[1:]):
        lst.append(f"file '../frames/e{i.lower()}_{st}.png'\nduration {max(t1 - t0, 0.04):.3f}")
    lst.append(f"file '../frames/e{i.lower()}_{bt[-2][0]}.png'")
    (OUT / f'l{i}.txt').write_text('\n'.join(lst))
    D = sc['dur'] + XF
    run(f"ffmpeg -loglevel error -y -f concat -safe 0 -i {OUT}/l{i}.txt -vf \"fps={FPS},scale=w='trunc({W}*(1+0.035*t/{D:.2f})/2)*2':h=-2:eval=frame,crop={W}:{H},format=yuv420p\" -t {D:.3f} -c:v libx264 -preset veryfast -crf 16 {OUT}/s{i}.mp4")

# ---- unir escenas con transición
off = 0; inputs = ''; chain = ''; last = '[0:v]'
for k, sc in enumerate(timeline):
    inputs += f' -i {OUT}/s{sc["i"]}.mp4'
starts = []
t = 0
for k, sc in enumerate(timeline):
    starts.append(t); t += sc['dur']
total = t
for k in range(1, len(timeline)):
    off = starts[k] - 0  # el cruce empieza cuando termina la voz de la escena anterior
    out = f'[x{k}]'
    trans = 'slideleft' if k % 2 else 'fade'
    chain += f'{last}[{k}:v]xfade=transition={trans}:duration={XF}:offset={off:.3f}{out};'
    last = out
chain = chain.rstrip(';')
run(f'ffmpeg -loglevel error -y {inputs} -filter_complex "{chain}" -map "{last}" -c:v libx264 -preset veryfast -crf 16 {OUT}/joined.mp4')

# ---- audio: voz + música con ducking + efectos
json.dump(dict(starts=starts, total=total), open(OUT / 'starts.json', 'w'))
vlist = '\n'.join(f"file 'v{sc['i']}.wav'" for sc in timeline)
(OUT / 'vlist.txt').write_text(vlist)
run(f'ffmpeg -loglevel error -y -f concat -safe 0 -i {OUT}/vlist.txt -c copy {OUT}/voice.wav')
sfx = []
for k, sc in enumerate(timeline):
    if k: sfx.append(('whoosh', starts[k] - 0.25))
    for st, tb in sc['beats'][1:]:
        sfx.append(('pop', starts[k] + tb))
ins = ' '.join(f'-i sfx/{n}.wav' for n, _ in sfx)
mix = ''.join(f'[{j + 2}]adelay={int(t * 1000)}|{int(t * 1000)},volume={0.55 if n == "pop" else 0.7}[f{j}];' for j, (n, t) in enumerate(sfx))
mix += f"[1]volume=0.22,atrim=0:{total + 1:.2f}[mus];[mus][0]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];"
mix += '[0][duck]' + ''.join(f'[f{j}]' for j in range(len(sfx))) + f'amix=inputs={len(sfx) + 2}:normalize=0:duration=first[m];[m]loudnorm=I=-14:TP=-1.5:LRA=11[a]'
run(f'ffmpeg -loglevel error -y -i {OUT}/voice.wav -i music/bed.wav {ins} -filter_complex "{mix}" -map "[a]" -ar 48000 -ac 2 {OUT}/mix.wav')
print('total', round(total, 1))
