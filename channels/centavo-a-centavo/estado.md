# Estado del proyecto (viernes 23 oct 2026)

Canal: **Centavo a Centavo** (@centavoacentavolatam), finanzas en español para latinos en EE. UU., sin cara, voz propia. Ritmo: 2 videos largos por semana (martes y viernes, 6 p. m. Bogotá).

## Publicado y programado
- Video 1 (crédito desde cero): https://youtu.be/Scik0zewZKk. 3 Shorts: 18, 20 y 22 oct (el calendario tuvo un Short el sáb 24; ver shorts-publicacion.md del video 1).
- Video 2 (subir puntaje: qué sí y qué no): https://youtu.be/038sz3wK3RU, público el 23 oct, miniatura "4 Sí / 3 No" asignada. Shorts: https://youtu.be/_c1eea1BPr0 (dom 25) y https://youtu.be/hUi-hdUP6r4 (lun 26).

## Pendiente de Andres en Studio (la API no lo permite)
- Fijar el comentario del video 2.
- Idioma Español y contenido alterado o sintético "No" en los videos y Shorts. Dejar Español y Educación como valores predeterminados de subida.
- Revisar los subtítulos del video 2 si cambió palabras al grabar (salen del guion, no de reconocimiento de voz).

## Siguiente
- Video 3, "Crédito con ITIN: bancos y tarjetas que lo aceptan", martes 27 oct. Primero verificar qué emisores aceptan ITIN y escribir el guion; audios 3 a 4 días antes.
- Pendientes de negocio: kit de crédito (17 USD) y diagnóstico 1:1 (47 a 67 USD) todavía no existen. Plan completo: investigacion/plan-30-dias.md.

## Cómo se edita (para repetirlo)
- Scripts en `videos/NN-.../edicion/`: align.py (alinea guion y voz por pausas, sin ASR), states2.py (gráficos SVG), compose.py y final.py (ffmpeg, subtítulos karaoke, barra de progreso, loudnorm -14), shorts2.py. Un audio por escena, guion en locucion.md.
- Publicar y subir se hace con la sesión Remote Control en el PC de Andres, solo con sus palabras explícitas. Chrome no adjunta más de 10 MB.
- YouTube está bloqueado desde la nube; ASR sin acceso a red.
