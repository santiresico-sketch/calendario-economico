# -*- coding: utf-8 -*-
"""Genera ar.ics y uy.ics (calendario economico AR/UY, fuentes oficiales).
Ventana movil: proximos ~13 meses desde HOY. Confirmadas (dict OV) > estimadas por patron."""
import datetime as dt, calendar, hashlib, os
TODAY = dt.date.today(); HORIZON = TODAY + dt.timedelta(days=400)
GEN = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
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
def pmn(y,m,n=1):
    mm,yy=m-n,y
    while mm<=0: mm+=12; yy-=1
    return f"{MES[mm]} {yy}"
def qref(y,m): return f"{ {3:'4to',6:'1er',9:'2do',12:'3er'}[m] } trimestre { {3:y-1,6:y,9:y,12:y}[m] }"
U=dict(ipc_ar="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31",emae_ar="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-9-48",
 ica_ar="https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-2-40",pbi_ar="https://www.indec.gob.ar/indec/web/Nivel3-Tema-3-9",
 bdp_ar="https://www.indec.gob.ar/indec/web/Nivel3-Tema-3-13",fiscal_ar="https://www.argentina.gob.ar/economia/sechacienda/calendariodepublicacion",
 cambios_ar="https://www.bcra.gob.ar/calendario-de-informes/",rem_ar="https://www.bcra.gob.ar/publicacionesestadisticas/relevamiento_expectativas_de_mercado.asp",
 ipc_uy="https://www.gub.uy/instituto-nacional-estadistica/indice-precios-consumo",
 imae_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Informe-del-Indicador-Mensual-de-Actividad-Economica-(IMAE).aspx",
 ext_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Cuentas-Nacionales-e-Internacionales.aspx",
 pbi_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/informe-trimestral-cuentas-nacionales.aspx",
 bdp_uy="https://www.bcu.gub.uy/Estadisticas-e-Indicadores/Paginas/Cuentas-Nacionales-e-Internacionales.aspx",
 fiscal_uy="https://www.gub.uy/ministerio-economia-finanzas/tematica/resultados-del-sector-publico")
NAME=dict(ipc_ar=("AR","Inflacion - IPC","INDEC"),emae_ar=("AR","Actividad - EMAE","INDEC"),ica_ar=("AR","Balanza comercial - ICA","INDEC"),
 pbi_ar=("AR","PBI trimestral - Cuentas Nacionales","INDEC"),bdp_ar=("AR","Balanza de Pagos / PII / Deuda externa","INDEC"),
 fiscal_ar=("AR","Resultado fiscal Sector Publico Nacional","Min. Economia (Sec. Hacienda)"),
 cambios_ar=("AR","Mercado de Cambios y Balance Cambiario","BCRA"),rem_ar=("AR","REM - Expectativas de Mercado","BCRA"),
 ipc_uy=("UY","Inflacion - IPC","INE"),imae_uy=("UY","Actividad - IMAE","BCU"),ext_uy=("UY","Comercio exterior de bienes","BCU"),
 pbi_uy=("UY","PBI trimestral - Cuentas Nacionales","BCU"),bdp_uy=("UY","Balanza de Pagos","BCU"),fiscal_uy=("UY","Resultado fiscal Sector Publico","MEF"))
D=dt.date
OV={("ipc_ar",2026,7):D(2026,7,14),("ipc_ar",2026,8):D(2026,8,13),("ipc_ar",2026,9):D(2026,9,10),("ipc_ar",2026,10):D(2026,10,13),("ipc_ar",2026,11):D(2026,11,12),("ipc_ar",2026,12):D(2026,12,15),
 ("emae_ar",2026,6):D(2026,6,29),("emae_ar",2026,7):D(2026,7,22),("emae_ar",2026,8):D(2026,8,20),("emae_ar",2026,9):D(2026,9,24),("emae_ar",2026,10):D(2026,10,21),("emae_ar",2026,11):D(2026,11,24),("emae_ar",2026,12):D(2026,12,21),
 ("ica_ar",2026,7):D(2026,7,20),("ica_ar",2026,8):D(2026,8,20),("ica_ar",2026,9):D(2026,9,18),("ica_ar",2026,10):D(2026,10,19),("ica_ar",2026,11):D(2026,11,19),("ica_ar",2026,12):D(2026,12,18),
 ("cambios_ar",2026,6):D(2026,6,26),("cambios_ar",2026,7):D(2026,7,31),("cambios_ar",2026,8):D(2026,8,28),("cambios_ar",2026,9):D(2026,9,25),("cambios_ar",2026,10):D(2026,10,30),("cambios_ar",2026,11):D(2026,11,27),("cambios_ar",2026,12):D(2026,12,31),
 ("rem_ar",2026,7):D(2026,7,6),("rem_ar",2026,8):D(2026,8,6),("rem_ar",2026,9):D(2026,9,4),("rem_ar",2026,10):D(2026,10,6),("rem_ar",2026,11):D(2026,11,5),
 ("ipc_uy",2026,7):D(2026,7,3),("ipc_uy",2026,8):D(2026,8,5),
 ("pbi_ar",2026,9):D(2026,9,17),("pbi_ar",2026,12):D(2026,12,16),
 ("bdp_ar",2026,6):D(2026,6,24),("bdp_ar",2026,9):D(2026,9,29),("bdp_ar",2026,12):D(2026,12,22)}
events=[]
def emit(key,y,m,patd,period,time=None):
    conf=(key,y,m) in OV; date=OV.get((key,y,m),patd)
    if not (TODAY<=date<=HORIZON): return
    c,ind,org=NAME[key]; events.append((c,ind,org,date,period,U[key],conf,time))
win=[];yy,mm=TODAY.year,TODAY.month
for _ in range(15):
    win.append((yy,mm)); mm+=1
    if mm>12: mm=1;yy+=1
T16="16:00"
for (y,m) in win:
    emit("ipc_ar",y,m,dayw(y,m,13),pmn(y,m,1),T16); emit("emae_ar",y,m,dayw(y,m,22),pmn(y,m,2),T16)
    emit("ica_ar",y,m,dayw(y,m,19),pmn(y,m,1),T16); emit("fiscal_ar",y,m,dayw(y,m,18),pmn(y,m,1))
    emit("cambios_ar",y,m,lfri(y,m),pmn(y,m,1)); emit("rem_ar",y,m,dayw(y,m,5),pmn(y,m,1))
    emit("ipc_uy",y,m,dayw(y,m,4),pmn(y,m,1)); emit("imae_uy",y,m,lbd(y,m),pmn(y,m,2))
    emit("ext_uy",y,m,lbd(y,m),pmn(y,m,1)); emit("fiscal_uy",y,m,lbd(y,m),pmn(y,m,1))
    if m in (3,6,9,12):
        emit("pbi_ar",y,m,dayw(y,m,17),qref(y,m),T16); emit("bdp_ar",y,m,dayw(y,m,24),qref(y,m),T16)
        emit("pbi_uy",y,m,dayw(y,m,15),qref(y,m)); emit("bdp_uy",y,m,lbd(y,m),qref(y,m))
def esc(s): return s.replace("\\","\\\\").replace(",","\\,").replace(";","\\;").replace("\n","\\n")
def fold(line):
    out=[]
    while len(line.encode("utf-8"))>75:
        cut=75
        while len(line[:cut].encode("utf-8"))>75: cut-=1
        out.append(line[:cut]); line=" "+line[cut:]
    out.append(line); return "\r\n".join(out)
def build(pais,calname,cname,chex,outfile):
    evs=[e for e in events if e[0]==pais]; evs.sort(key=lambda e:(e[3],e[1]))
    L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Calendario Economico AR-UY//ES//","CALSCALE:GREGORIAN",
       "X-WR-CALNAME:"+calname,"X-WR-TIMEZONE:America/Argentina/Buenos_Aires","COLOR:"+cname,"X-APPLE-CALENDAR-COLOR:"+chex,
       "REFRESH-INTERVAL;VALUE=DURATION:PT12H","X-PUBLISHED-TTL:PT12H",
       "X-WR-CALDESC:Publicaciones economicas oficiales. Fuente: organismos oficiales de "+("Argentina" if pais=="AR" else "Uruguay")+"."]
    for c,ind,org,date,period,url,conf,time in evs:
        paisn="Argentina" if c=="AR" else "Uruguay"
        estado="Confirmada (calendario oficial)" if conf else "Estimada por patron - a confirmar"
        pref="" if conf else "~ "
        summ=f"{pref}{ind} ({org})"
        uid=hashlib.md5(f"{c}|{ind}|{date.isoformat()}|{org}".encode()).hexdigest()+"@cal-econ-aruy"
        desc=f"Pais: {paisn}\\nIndicador: {ind}\\nOrganismo: {org}\\nPeriodo de referencia: dato de {period}\\nEstado de la fecha: {estado}\\nFuente oficial: {url}"
        L+= ["BEGIN:VEVENT",f"UID:{uid}",f"DTSTAMP:{GEN}","SEQUENCE:0"]
        if time:
            hh,mm2=time.split(":"); uh=int(hh)+3
            L+=[f"DTSTART:{date.strftime('%Y%m%d')}T{uh:02d}{mm2}00Z",f"DTEND:{date.strftime('%Y%m%d')}T{uh:02d}3000Z"]; trig="-PT30M"
        else:
            L+=[f"DTSTART;VALUE=DATE:{date.strftime('%Y%m%d')}",f"DTEND;VALUE=DATE:{(date+dt.timedelta(days=1)).strftime('%Y%m%d')}"]; trig="-PT15H"
        L+= ["SUMMARY:"+esc(summ),"DESCRIPTION:"+esc(desc),"URL:"+url,"CATEGORIES:"+paisn,
             ("STATUS:CONFIRMED" if conf else "STATUS:TENTATIVE"),"TRANSP:TRANSPARENT",
             "BEGIN:VALARM","ACTION:DISPLAY","DESCRIPTION:Recordatorio",f"TRIGGER:{trig}","END:VALARM","END:VEVENT"]
    L.append("END:VCALENDAR")
    open(outfile,"w",encoding="utf-8").write("\r\n".join(fold(x) for x in L)+"\r\n")
    print(f"{outfile}: {len(evs)} eventos")
build("AR","Economia Argentina","cornflowerblue","#4F8DE0","ar.ics")
build("UY","Economia Uruguay","darkorange","#E8820C","uy.ics")
