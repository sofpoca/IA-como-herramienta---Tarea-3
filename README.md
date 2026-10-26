#IA como Herramienta, no como Autor: Desarrollo Guiado y Validado de un Script en Python
## Casos de prueba del analizador

Los archivos de prueba se ecnuentrran en la carpeta de `Anlizador_logs`
Para ejecutar cada caso, inicia el analizador, selecciona el archivo indicado y
responde `sí` cuando pregunte si deseas ver el detalle.



## 1. Archivo bien formado: `logs_bien_formado.txt`

Contiene tres registros con severidad reconocida, fecha real en formato
`YYYY-MM-DD` y mensaje no vacío.

**Resultado esperado**
<img width="567" height="572" alt="image" src="https://github.com/user-attachments/assets/4647bfb0-131a-4300-a448-eacf5171a574" />
- Total de eventos: 3.
- INFO: 1, WARNING: 1, ERROR: 1.
- Líneas incompletas o mal formateadas: 0.
- En el detalle, las tres líneas deben aparecer como completas.
- 
**Resultado obtenido**

Se analizó el archivo con `analyze_lines`: se obtuvieron 3 resultados, conteos
`INFO=1`, `WARNING=1`, `ERROR=1` y 0 líneas incompletas. Cada resultado tuvo
fecha válida y estado completo.



## 2. Archivo con errores e inconsistencias: `logs_con_inconsistencias.txt`

Incluye una fecha inexistente, una fecha ausente, un mensaje ausente, una
severidad no admitida y líneas vacías o con solo espacios.

**Resultado esperado**

<img width="602" height="667" alt="image" src="https://github.com/user-attachments/assets/a1d07fa8-34c8-4724-8c06-d18ccd22a5ac" />


- Las líneas vacías se ignoran y no aparecen en el detalle.
- Total de eventos: 3
- INFO: 1, WARNING: 1, ERROR: 1. La línea DEBUG no cuenta como evento porque la severidad no está reconocida.
- Líneas incompletas o mal formateadas: 4.
- Las cuatro líneas con contenido aparecen incompletas en el detalle, con su
  numeración original: 1, 2, 3 y 4.
  

**Resultado obtenido**

Se analizó el archivo con `analyze_lines`: se obtuvieron 4 resultados (se
ignoraron las líneas 5 y 6), conteos `INFO=1`, `WARNING=1`, `ERROR=1` y 4
líneas incompletas. Las líneas se conservaron numeradas como 1, 2, 3 y 4.
La línea 1 fue marcada con fecha inválida; la 2, con fecha ausente; la 3, con
mensaje vacío; y la 4, con severidad no reconocida.



## 3. Archivo con logs mixtos: `pruebas_logs.txt`

**Resultado esperado**
<img width="532" height="202" alt="image" src="https://github.com/user-attachments/assets/ab3d8cb8-6665-4cfb-84c8-a0763ccedf37" />

<img width="520" height="867" alt="image" src="https://github.com/user-attachments/assets/88beca30-279f-45e0-beea-d22c3614afee" />

- Total de eventos: 7. Solo cuentan las líneas con severidad reconocida: [INFO], [WARNING] o [ERROR].
- INFO: 3, WARNING: 2, ERROR: 2.
- Líneas incompletas o mal formateadas: 5.
- La línea con [DEBUG] se marca como incompleta, pero no cuenta como evento.
- No hay líneas vacías que deban ignorarse.

**Resultados obtenidos**
El analizador obtiene los mismos conteos esperados: 7 eventos —3 INFO, 2 WARNING y 2 ERROR— y 5 líneas incompletas.


## Verificación

Los resultados obtenidos se comprobaron directamente con las funciones de
análisis del programa, incluyendo los conteos, los estados de cada línea y la
omisión de renglones vacíos. La presentación del resumen y el detalle depende
de la respuesta ingresada durante la ejecución interactiva.
