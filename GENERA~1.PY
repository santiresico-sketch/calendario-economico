# -*- coding: utf-8 -*-
"""
Genera calendario(s) economico(s) (.ics) de Argentina y Uruguay con publicaciones oficiales.
Solo fuentes oficiales: INDEC, BCRA, Min. Economia (AR) / INE, BCU, MEF (UY).

DISENO "VENTANA MOVIL": en cada ejecucion arma los proximos ~13 meses contados desde HOY.
- Las fechas CONFIRMADAS (calendario de difusion oficial) estan en el dict OV y tienen prioridad.
- El resto se completa por PATRON (estimadas, STATUS TENTATIVE, prefijo ~).
Asi el feed nunca se queda sin fechas aunque pase el tiempo.

Variables de entorno:
  OUTLOOK=1  -> variante compatible con Outlook (sin emojis, sin METHOD, recordatorio negativo)
  PAIS=AR|UY -> genera solo ese pais (archivo y color separados). Sin PAIS = ambos juntos.
"""
import datetime as dt, calendar, hashlib, os

OUTLOOK = os.environ.get("OUTLOOK") == "1"
PAIS = os.environ.get("PAIS")
suf = "_argentina" if PAIS=="AR" else "_uruguay" if PAIS=="UY" else ("_outlook" if OUTLOOK else "")
fname = f"calendario_economico_ar_uy{suf}.ics"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
GEN_STAMP = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
TODAY = dt.date.today()
HORIZON = TODAY + dt.timedelta(days=400)

def lbd(y,m):
    d=dt.date(y,m,calendar.monthrange(y,m)[1])
    while d.weekday()>=5: d-=dt.timedelta(days=1)
    return d
def lfri(y,m):
    d=dt.date(y,m,calendar.monthrange(y,m)[1])
    while d.weekday()!=4: d-=dt.timedelta(days=1)
    return d
def tw(d):
    while d.weekday()>=5: d+=dt.timedelta(days=1)
    return d
def dayw(y,m,day): return tw(dt.date(y,m,day))

MES={1:"enero",2:"febrero",3:"marzo",4:"abril",5:"mayo",6:"junio",7:"julio",8:"agosto",9:"septiembre",10:"octubre",11:"noviembre",12:"diciembre"}
def prevmn(y,m,n=1):
    mm,yy=m-n,y
    while mm<=0: mm+=12; yy-=1
    return f"{MES[mm]} {yy}"
def qref(y,m):
    return {3:("4to",y-1),6:("1er",y),9:("2do",y),12:("3er",y)}[m] and \
           f"{ {3:'4to',6:'1er',9:'2do',12:'3er'}[m] } trimestre { {3:y-1,6:y,9:y,12:y}[m] }"

U=dict(
 ipc_ar="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31",
 emae_ar="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48",
 ica_ar="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-2-40",
 pbi_ar="https://www.indec.gob.ar/indec/web/Nivel3-Tema-3-9",
 bdp_ar="https://www.indec.gob.ar/indec/web/Nivel3-Tema-3-13",
 fiscal_ar="https://www.argentina.gob.ar/economia/sechacienda/calendariodepublicacion",
 cambios_ar="https://www.bcra.gob.ar/calendario-de-informes/",
 rem_ar="https://www.bcra.gob.ar/publicacionesestadisticas/relevamiento_expectativas_de_mercado.asp",
 ipc_uy="https://www.gub.uy/instituto-nacional-estadistica/indice-precios-consumo",
 imae_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Informe-del-Indicador-Mensual-de-Actividad-Economica-(IMAE).aspx",
 ext_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Cuentas-Nacionales-e-Internacionales.aspx",
 bdp_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Cuentas-Nacionales-e-Internacionales.aspx",
 pbi_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/informe-trimestral-cuentas-nacionales.aspx",
 fiscal_uy="https://www.gub.uy/ministerio-economia-finanzas/tematica/resultados-del-sector-publico",
)
NAME=dict(
 ipc_ar=("AR","Inflacion - IPC","INDEC"), emae_ar=("AR","Actividad - EMAE","INDEC"),
 ica_ar=("AR","Balanza comercial - ICA","INDEC"), pbi_ar=("AR","PBI trimestral - Cuentas Nacionales","INDEC"),
 bdp_ar=("AR","Balanza de Pagos / PII / Deuda externa","INDEC"),
 fiscal_ar=("AR","Resultado fiscal Sector Publico Nacional","Min. Economia (Sec. Hacienda)"),
 cambios_ar=("AR","Mercado de Cambios y Balance Cambiario","BCRA"),
 rem_ar=("AR","REM - Expectativas de Mercado","BCRA"),
 ipc_uy=("UY","Inflacion - IPC","INE"), imae_uy=("UY","Actividad - IMAE","BCU"),
 ext_uy=("UY","Comercio exterior de bienes","BCU"), pbi_uy=("UY","PBI trimestral - Cuentas Nacionales","BCU"),
 bdp_uy=("UY","Balanza de Pagos","BCU"),
 fiscal_uy=("UY","Resultado fiscal Sector Publico","MEF"),
)
D=dt.date
# Fechas CONFIRMADAS del calendario oficial (prioridad sobre el patron)
OV={
 ("ipc_ar",2026,7):D(2026,7,14),("ipc_ar",2026,8):D(2026,8,13),("ipc_ar",2026,9):D(2026,9,10),("ipc_ar",2026,10):D(2026,10,13),("ipc_ar",2026,11):D(2026,11,12),("ipc_ar",2026,12):D(2026,12,15),
 ("emae_ar",2026,6):D(2026,6,29),("emae_ar",2026,7):D(2026,7,22),("emae_ar",2026,8):D(2026,8,20),("emae_ar",2026,9):D(2026,9,24),("emae_ar",2026,10):D(2026,10,21),("emae_ar",2026,11):D(2026,11,24),("emae_ar",2026,12):D(2026,12,21),
 ("ica_ar",2026,7):D(2026,7,20),("ica_ar",2026,8):D(2026,8,20),("ica_ar",2026,9):D(2026,9,18),("ica_ar",2026,10):D(2026,10,19),("ica_ar",2026,11):D(2026,11,19),("ica_ar",2026,12):D(2026,12,18),
 ("cambios_ar",2026,6):D(2026,6,26),("cambios_ar",2026,7):D(2026,7,31),("cambios_ar",2026,8):D(2026,8,28),("cambios_ar",2026,9):D(2026,9,25),("cambios_ar",2026,10):D(2026,10,30),("cambios_ar",2026,11):D(2026,11,27),("cambios_ar",2026,12):D(2026,12,31),
 ("rem_ar",2026,7):D(2026,7,6),("rem_ar",2026,8):D(2026,8,6),("rem_ar",2026,9):D(2026,9,4),("rem_ar",2026,10):D(2026,10,6),("rem_ar",2026,11):D(2026,11,5),
 ("ipc_uy",2026,7):D(2026,7,3),("ipc_uy",2026,8):D(2026,8,5),
 ("pbi_ar",2026,9):D(2026,9,17),("pbi_ar",2026,12):D(2026,12,16),
 ("bdp_ar",2026,6):D(2026,6,24),("bdp_ar",2026,9):D(2026,9,29),("bdp_ar",2026,12):D(2026,12,22),
}

events=[]
def emit(key, y, m, patdate, period, time=None):
    conf = (key,y,m) in OV
    date = OV[(key,y,m)] if conf else patdate
    if not (TODAY <= date <= HORIZON): return
    c,ind,org = NAME[key]
    events.append(dict(country=c,indicador=ind,organismo=org,date=date,period=period,url=U[key],confirmed=conf,time=time))

# ventana de meses desde hoy
win=[]; yy,mm=TODAY.year,TODAY.month
for _ in range(15):
    win.append((yy,mm)); mm+=1
    if mm>12: mm=1; yy+=1

T16="16:00"
for (y,m) in win:
    # mensuales AR
    emit("ipc_ar",y,m, dayw(y,m,13), prevmn(y,m,1), T16)
    emit("emae_ar",y,m, dayw(y,m,22), prevmn(y,m,2), T16)
    emit("ica_ar",y,m, dayw(y,m,19), prevmn(y,m,1), T16)
    emit("fiscal_ar",y,m, dayw(y,m,18), prevmn(y,m,1))
    emit("cambios_ar",y,m, lfri(y,m), prevmn(y,m,1))
    emit("rem_ar",y,m, dayw(y,m,5), prevmn(y,m,1))
    # mensuales UY
    emit("ipc_uy",y,m, dayw(y,m,4), prevmn(y,m,1))
    emit("imae_uy",y,m, lbd(y,m), prevmn(y,m,2))
    emit("ext_uy",y,m, lbd(y,m), prevmn(y,m,1))
    emit("fiscal_uy",y,m, lbd(y,m), prevmn(y,m,1))
    # trimestrales (meses de publicacion 3,6,9,12)
    if m in (3,6,9,12):
        emit("pbi_ar",y,m, dayw(y,m,17), qref(y,m), T16)
        emit("bdp_ar",y,m, dayw(y,m,24), qref(y,m), T16)
        emit("pbi_uy",y,m, dayw(y,m,15), qref(y,m))
        emit("bdp_uy",y,m, lbd(y,m), qref(y,m))

if PAIS in ("AR","UY"):
    events=[e for e in events if e["country"]==PAIS]

def esc(s): return s.replace("\\","\\\\").replace(",","\\,").replace(";","\\;").replace("\n","\\n")
def fold(line):
    out=[]
    while len(line.encode("utf-8"))>75:
        cut=75
        while len(line[:cut].encode("utf-8"))>75: cut-=1
        out.append(line[:cut]); line=" "+line[cut:]
    out.append(line); return "\r\n".join(out)

fAR="\U0001F1E6\U0001F1F7"; fUY="\U0001F1FA\U0001F1FE"
if PAIS=="AR": calname="Economia Argentina"; cname="cornflowerblue"; chex="#4F8DE0"
elif PAIS=="UY": calname="Economia Uruguay"; cname="darkorange"; chex="#E8820C"
else: calname="Calendario Economico Argentina y Uruguay"; cname=None; chex=None

H=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Calendario Economico AR-UY//ES//","CALSCALE:GREGORIAN"]
if not OUTLOOK and PAIS is None: H.append("METHOD:PUBLISH")
H+= ["X-WR-CALNAME:"+calname,"X-WR-TIMEZONE:America/Argentina/Buenos_Aires"]
if cname: H+=["COLOR:"+cname,"X-APPLE-CALENDAR-COLOR:"+chex]
H.append("REFRESH-INTERVAL;VALUE=DURATION:PT12H"); H.append("X-PUBLISHED-TTL:PT12H")
H.append("X-WR-CALDESC:Publicaciones economicas oficiales. Fuentes: INDEC\\, BCRA\\, Min. Economia (AR) - INE\\, BCU\\, MEF (UY).")

lines=list(H)
events.sort(key=lambda e:(e["date"],e["country"],e["indicador"]))
use_emoji=(not OUTLOOK) and (PAIS is None)
for e in events:
    if use_emoji: tag=(fAR if e["country"]=="AR" else fUY)+" "
    elif PAIS is None: tag=("[AR] " if e["country"]=="AR" else "[UY] ")
    else: tag=""
    pais="Argentina" if e["country"]=="AR" else "Uruguay"
    estado="Confirmada (calendario oficial)" if e["confirmed"] else "Estimada por patron - a confirmar"
    pref="" if e["confirmed"] else "~ "
    summ=f"{tag}{pref}{e['indicador']} ({e['organismo']})"
    uid=hashlib.md5(f"{e['country']}|{e['indicador']}|{e['date'].isoformat()}|{e['organismo']}".encode()).hexdigest()+"@cal-econ-aruy"
    desc=(f"Pais: {pais}\\nIndicador: {e['indicador']}\\nOrganismo: {e['organismo']}\\n"
          f"Periodo de referencia: dato de {e['period']}\\nEstado de la fecha: {estado}\\nFuente oficial: {e['url']}")
    lines+= ["BEGIN:VEVENT",f"UID:{uid}",f"DTSTAMP:{GEN_STAMP}","SEQUENCE:0"]
    if e["time"]:
        hh,mm=e["time"].split(":"); uh=int(hh)+3
        lines+=[f"DTSTART:{e['date'].strftime('%Y%m%d')}T{uh:02d}{mm}00Z",f"DTEND:{e['date'].strftime('%Y%m%d')}T{uh:02d}3000Z"]; trig="-PT30M"
    else:
        lines+=[f"DTSTART;VALUE=DATE:{e['date'].strftime('%Y%m%d')}",f"DTEND;VALUE=DATE:{(e['date']+dt.timedelta(days=1)).strftime('%Y%m%d')}"]; trig="-PT15H" if (OUTLOOK or PAIS) else "PT9H"
    lines+= ["SUMMARY:"+esc(summ),"DESCRIPTION:"+esc(desc),"URL:"+e["url"],"CATEGORIES:"+pais,
             ("STATUS:CONFIRMED" if e["confirmed"] else "STATUS:TENTATIVE"),"TRANSP:TRANSPARENT",
             "BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:Recordatorio",f"TRIGGER:{trig}","END:VALARM","END:VEVENT"]
lines.append("END:VCALENDAR")
open(OUT,"w",encoding="utf-8").write("\r\n".join(fold(l) for l in lines)+"\r\n")
conf=sum(1 for e in events if e["confirmed"])
print(f"{fname} -> {len(events)} eventos (confirmados {conf}, estimados {len(events)-conf}) | rango {min((e['date'] for e in events), default='-')} .. {max((e['date'] for e in events), default='-')}")
