import math, json
F='font-family="Inter Display, Inter, sans-serif"'
DEFS='<defs><radialGradient id="bg" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#14805A"/><stop offset="1" stop-color="#083D2C"/></radialGradient><linearGradient id="coin" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFE08A"/><stop offset="0.55" stop-color="#F5B92E"/><stop offset="1" stop-color="#D9921A"/></linearGradient><linearGradient id="leaf" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#7EE2A8"/><stop offset="1" stop-color="#C8F7D9"/></linearGradient></defs>'
def svg(body,mark=True):
    m=f'<text x="1840" y="1040" text-anchor="end" {F} font-size="26" font-weight="600" fill="#9BE8BC" opacity="0.7">Centavo a Centavo</text>' if mark else ''
    return f'<svg id="s" xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">{DEFS}<rect width="1920" height="1080" fill="url(#bg)"/>{body}{m}</svg>'
# NOTE: content kept in upper ~800px; bottom band reserved for captions
def title(t,y=150,s=72): return f'<text x="960" y="{y}" text-anchor="middle" {F} font-weight="800" font-size="{s}" fill="#fff">{t}</text>'
def step(n): return f'<rect x="80" y="60" width="250" height="64" rx="32" fill="#F5B92E"/><text x="205" y="104" text-anchor="middle" {F} font-weight="800" font-size="34" fill="#0A4A35">PASO {n} DE 6</text>'
def card(x,y,w,h,big,small,fill='#0A3A2A',tc='#fff',sc='#C8F7D9',stroke='#7EE2A8',bs=60):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="36" fill="{fill}" stroke="{stroke}" stroke-width="5"/><text x="{x+w/2}" y="{y+h/2-4}" text-anchor="middle" {F} font-weight="800" font-size="{bs}" fill="{tc}">{big}</text><text x="{x+w/2}" y="{y+h/2+56}" text-anchor="middle" {F} font-weight="500" font-size="36" fill="{sc}">{small}</text>'
def coin(x,y,s):
    return f'<g transform="translate({x} {y}) scale({s}) translate(-400 -440)"><path d="M400 268 C400 230 402 205 408 180" stroke="#9BE8BC" stroke-width="16" fill="none" stroke-linecap="round"/><path d="M406 196 C 430 140, 500 125, 548 140 C 530 190, 470 222, 406 196 Z" fill="url(#leaf)"/><path d="M402 214 C 380 170, 320 150, 270 168 C 290 214, 350 236, 402 214 Z" fill="url(#leaf)" opacity="0.92"/><circle cx="400" cy="450" r="196" fill="url(#coin)"/><circle cx="400" cy="450" r="164" fill="none" stroke="#B87812" stroke-width="10" opacity="0.55"/><text x="400" y="450" text-anchor="middle" dominant-baseline="central" {F} font-weight="800" font-size="250" fill="#0A4A35">¢</text></g>'
S={}
G='#7EE2A8'; R='#FF8A7A'; Y='#F5B92E'
def chip(lbl,ok=True):
    c=Y if ok else R; fg='#0A4A35' if ok else '#3A1010'
    return f'<rect x="80" y="60" width="230" height="70" rx="35" fill="{c}"/><text x="195" y="109" text-anchor="middle" {F} font-weight="800" font-size="38" fill="{fg}">{lbl}</text>'
def line(t,y,s=54,fill='#C8F7D9',w=600): return f'<text x="960" y="{y}" text-anchor="middle" {F} font-weight="{w}" font-size="{s}" fill="{fill}">{t}</text>'
red=dict(fill='#3A1E1E',stroke=R,sc='#FFD2CB')
# e01
H1=title('¿Puntaje de crédito bajo?',250,92)
okc=lambda x,t: f'<rect x="{x}" y="370" width="780" height="300" rx="40" fill="#0A3A2A" stroke="{G}" stroke-width="6"/><text x="{x+390}" y="500" text-anchor="middle" {F} font-weight="800" font-size="150" fill="{G}">4</text><text x="{x+390}" y="600" text-anchor="middle" {F} font-weight="700" font-size="52" fill="#fff">{t}</text>'
nok=lambda x,t: f'<rect x="{x}" y="370" width="780" height="300" rx="40" fill="#3A1E1E" stroke="{R}" stroke-width="6"/><text x="{x+390}" y="500" text-anchor="middle" {F} font-weight="800" font-size="150" fill="{R}">3</text><text x="{x+390}" y="600" text-anchor="middle" {F} font-weight="700" font-size="52" fill="#fff">{t}</text>'
S['e01_0']=svg(H1+line('Hay cosas que funcionan… y otras que no',420,60))
S['e01_1']=svg(H1+okc(570,'cosas que SÍ funcionan'))
S['e01_2']=svg(H1+okc(100,'cosas que SÍ funcionan')+nok(1040,'cosas que NO sirven'))
S['e01_3']=svg(title('La tercera baja más tu puntaje',330,84)+nok(570,'cosas que NO sirven').replace('y="370"','y="450"').replace('y="500"','y="580"').replace('y="600"','y="680"')+line('Quédate hasta el final',900,52,Y,700))
# e02
T2=title('¿Cuánto tarda de verdad?',200,80)
S['e02_0']=svg(T2+line('Nadie te lo puede prometer',420,60))
S['e02_1']=svg(T2+f'<rect x="360" y="330" width="1200" height="260" rx="40" fill="#3A1E1E" stroke="{R}" stroke-width="6"/><text x="960" y="490" text-anchor="middle" {F} font-weight="800" font-size="110" fill="{R}">+100 puntos en 1 semana</text>'+line('✗ Nadie puede prometértelo',690,56,'#FFD2CB',700))
cal=''.join(f'<rect x="{300+i*180}" y="360" width="150" height="150" rx="24" fill="{"#F5B92E" if i==0 else "#0A3A2A"}" stroke="{G}" stroke-width="4"/><text x="{375+i*180}" y="460" text-anchor="middle" {F} font-weight="800" font-size="54" fill="{"#0A4A35" if i==0 else "#fff"}">{m}</text>' for i,m in enumerate(['Ene','Feb','Mar','Abr','May','Jun','Jul'][:7]))
S['e02_2']=svg(T2+cal+line('Los bancos reportan más o menos 1 vez al mes',640,56,'#fff',700))
S['e02_3']=svg(T2+card(200,330,720,340,'~30 días','algunas cosas se notan',bs=90)+card(1000,330,720,340,'Meses','otras necesitan tiempo',bs=90))
# e03
T3=chip('SÍ 1')+title('Paga siempre a tiempo',230,84)
S['e03_0']=svg(T3+line('Lo más importante de tu puntaje',430,58))
S['e03_1']=svg(T3+f'<text x="960" y="550" text-anchor="middle" {F} font-weight="800" font-size="260" fill="{Y}">35 %</text>'+line('del puntaje es tu historial de pagos',660,56,'#fff',700))
S['e03_2']=svg(T3+card(260,330,640,330,'+30 días tarde','un pago atrasado',**red,bs=76)+f'<text x="960" y="520" text-anchor="middle" {F} font-weight="800" font-size="110" fill="{Y}">→</text>'+card(1020,330,640,330,'7 años','en tu reporte',**red,bs=100))
S['e03_3']=svg(T3+card(360,330,1200,330,'Pago automático','del mínimo en todas tus cuentas',bs=88)+line('✓ Un olvido no te cuesta caro',780,56,G,700))
# e04
T4=chip('SÍ 2')+title('Usa menos de tu límite',230,84)
def ubar(y,pct,col,lab): return f'<rect x="360" y="{y}" width="1200" height="100" rx="50" fill="#0A3A2A"/><rect x="360" y="{y}" width="{1200*pct/100:.0f}" height="100" rx="50" fill="{col}"/><text x="320" y="{y+70}" text-anchor="end" {F} font-weight="800" font-size="58" fill="#fff">{pct} %</text><text x="1590" y="{y+70}" {F} font-weight="700" font-size="46" fill="{col}">{lab}</text>'
S['e04_0']=svg(T4+line('Es lo que se nota más rápido',430,58))
S['e04_1']=svg(T4+line('Límite $1,000 · usados $900',360,62,'#fff',700)+ubar(430,90,R,'✗ muy alto'))
S['e04_2']=svg(T4+line('Límite $1,000 · usados $900',330,62,'#fff',700)+ubar(400,90,R,'✗')+ubar(550,30,'#FFE08A','~ ok'))
S['e04_3']=svg(T4+line('Límite $1,000 · usados $900',330,62,'#fff',700)+ubar(400,90,R,'✗')+ubar(550,30,'#FFE08A','~ ok')+ubar(700,10,G,'✓ mejor'))
S['e04_4']=svg(T4+card(300,330,1320,340,'Paga ANTES de la fecha de corte','ahí el banco reporta tu saldo',bs=76)+line('Tu reporte muestra un saldo bajo',790,56,Y,700))
# e05
S['e05_0']=svg(chip('SÍ 3')+title('Revisa tu reporte de crédito',230,80)+f'<rect x="360" y="330" width="1200" height="170" rx="40" fill="#fff"/><text x="960" y="440" text-anchor="middle" {F} font-weight="800" font-size="72" fill="#0A4A35">AnnualCreditReport.com</text>'+line('Gratis · sitio oficial',590,52))
S['e05_1']=svg(chip('SÍ 3')+title('Revisa tu reporte de crédito',230,80)+card(240,330,640,320,'Error real','deuda que no es tuya',**red,bs=72)+f'<text x="960" y="520" text-anchor="middle" {F} font-weight="800" font-size="110" fill="{Y}">→</text>'+card(1040,330,640,320,'Disputarlo','corregirlo puede subir el puntaje',bs=72))
T5=chip('SÍ 4')+title('No cierres tus tarjetas más antiguas',230,72)
S['e05_2']=svg(T5+card(360,330,1200,340,'Más años de historial','= mejor puntaje',bs=84))
S['e05_3']=svg(T5+card(360,330,1200,340,'Sin cuota anual','déjalas abiertas con un gasto pequeño',bs=84)+line('✓ Se quedan trabajando a tu favor',780,54,G,700))
# e06
T6=chip('NO 1',False)+title('Pagar para "borrar" tu mal crédito',230,72)
S['e06_0']=svg(title('Ahora, lo que NO sirve',420,100))
S['e06_1']=svg(T6+card(360,330,1200,340,'Dato negativo real','no se borra antes de tiempo',**red,bs=84))
S['e06_2']=svg(T6+card(360,300,1200,260,'Dato negativo real','no se borra antes de tiempo',**red,bs=64)+line('✓ Lo que sí es gratis: disputar errores',700,58,G,700))
T6b=chip('NO 2',False)+title('Cargar deuda para construir crédito',230,72)
S['e06_3']=svg(T6b+card(360,330,1200,340,'No es necesario','creerlo cuesta intereses',**red,bs=84))
S['e06_4']=svg(T6b+card(360,330,1200,340,'Paga el saldo completo','cada mes',bs=84)+line('= cero intereses',780,64,G,800))
# e07
T7=chip('NO 3',False)+title('Pedir muchas tarjetas a la vez',230,76)
S['e07_0']=svg(T7+line('La que más baja tu puntaje',430,64,'#fff',700))
S['e07_1']=svg(T7+card(360,330,1200,340,'1 solicitud = 1 consulta','aparece en tu reporte y resta un poco',**red,bs=76))
S['e07_2']=svg(T7+card(200,330,720,340,'Una sola','no es grave',bs=88))
S['e07_3']=svg(T7+card(200,330,720,340,'Una sola','no es grave',bs=88)+card(1000,330,720,340,'Varias en meses','sí se nota',**red,bs=76))
S['e07_4']=svg(T7+card(360,330,1200,340,'Pide solo lo que necesitas','y espacia las solicitudes',bs=76)+line('Más aún si tienes poco historial',780,52,Y,700))
# e08 resumen
yes=['Paga a tiempo','Usa menos del 30 % de tu límite','Revisa tu reporte','No cierres cuentas viejas']
no=['Promesas de "borrar" el mal crédito','Pedir muchas tarjetas a la vez']
def res(k):
    b=title('Resumen rápido',130,72); y=240
    for i,t in enumerate(yes):
        on=i<k
        b+=f'<circle cx="400" cy="{y+i*105}" r="34" fill="{G if on else "#0A3A2A"}" stroke="{G}" stroke-width="3"/><text x="400" y="{y+i*105+14}" text-anchor="middle" {F} font-weight="800" font-size="40" fill="{"#0A4A35" if on else G}">✓</text><text x="470" y="{y+i*105+16}" {F} font-weight="600" font-size="52" fill="#fff" opacity="{1 if on else 0.2}">{t}</text>'
    for i,t in enumerate(no):
        on=k-4>i; yy=y+(4+i)*105+20
        b+=f'<circle cx="400" cy="{yy}" r="34" fill="{R if on else "#3A1E1E"}" stroke="{R}" stroke-width="3"/><text x="400" y="{yy+14}" text-anchor="middle" {F} font-weight="800" font-size="40" fill="{"#3A1010" if on else R}">✗</text><text x="470" y="{yy+16}" {F} font-weight="600" font-size="52" fill="#fff" opacity="{1 if on else 0.2}">{t}</text>'
    return svg(b)
for k in range(7): S[f'e08_{k}']=res(k)
S['e08_7']=svg(title('¿Cuál de estas no sabías?',260,88)+f'<rect x="460" y="360" width="1000" height="200" rx="40" fill="#0A3A2A" stroke="{G}" stroke-width="5"/><text x="960" y="480" text-anchor="middle" {F} font-weight="700" font-size="58" fill="#fff">Cuéntame en los comentarios</text>')
S['e08_8']=svg(title('Próximo video',250,72)+card(360,330,1200,340,'Crédito con ITIN','cómo construirlo paso a paso',bs=88))
S['e08_9']=svg(coin(960,360,0.62)+f'<text x="960" y="680" text-anchor="middle" {F} font-weight="800" font-size="90" fill="#fff">Centavo a Centavo</text><rect x="760" y="720" width="400" height="90" rx="45" fill="#FF3B30"/><text x="960" y="780" text-anchor="middle" {F} font-weight="800" font-size="44" fill="#fff">SUSCRÍBETE</text>',mark=False)
for k,v in S.items(): open(f'frames/{k}.html','w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0}}</style></head><body>{v}</body></html>')
import json; json.dump(sorted(S),open('frames/list.json','w')); print(len(S))
