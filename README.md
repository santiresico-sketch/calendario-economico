# Calendario Económico Argentina y Uruguay

Feed de calendario (`.ics`) con las fechas de publicación de indicadores económicos oficiales de Argentina y Uruguay. Auto-actualizable y suscribible desde Google Calendar, Outlook o Apple Calendar.

**Fuentes oficiales:** INDEC, BCRA, Ministerio de Economía (Argentina) · INE, BCU, MEF (Uruguay).

## Indicadores incluidos

| Tipo | Argentina | Uruguay |
|---|---|---|
| Inflación (IPC) | INDEC | INE |
| Actividad mensual | EMAE (INDEC) | IMAE (BCU) |
| Fiscal mensual | Resultado SPN (Min. Economía) | Resultado Sector Público (MEF) |
| Mercado de cambios | Balance Cambiario (BCRA) | — |
| Expectativas de mercado | REM (BCRA) | — |
| Balanza comercial | ICA (INDEC) | Comercio exterior (BCU) |
| PBI trimestral | Cuentas Nacionales (INDEC) | Cuentas Nacionales (BCU) |
| Balanza de Pagos | INDEC | BCU |

Fechas **confirmadas** = del calendario de difusión oficial. Fechas **estimadas** (prefijo `~`, marcadas como tentativas) = derivadas del patrón de publicación de cada organismo; se confirman a medida que cada organismo publica su cronograma.

---

## 1. Publicar el repo (una sola vez)

1. Creá un repositorio **público** en GitHub (ej. `calendario-economico`).
2. Subí todo el contenido de esta carpeta (incluido `generar_calendario.py`, los `.ics`, `index.html` y la carpeta `.github/`).
3. Activá **GitHub Pages**: en el repo → **Settings → Pages** → en *Source* elegí **Deploy from a branch** → rama `main`, carpeta `/ (root)` → Save.
4. En **Settings → Actions → General → Workflow permissions**, marcá **Read and write permissions** (para que el robot pueda commitear las actualizaciones).

En ~1 minuto Pages te da una URL base: `https://TU-USUARIO.github.io/calendario-economico/`

## 2. URLs de suscripción

Reemplazá `TU-USUARIO` y `calendario-economico` por los tuyos:

- **Argentina:** `https://TU-USUARIO.github.io/calendario-economico/calendario_economico_ar_uy_argentina.ics`
- **Uruguay:** `https://TU-USUARIO.github.io/calendario-economico/calendario_economico_ar_uy_uruguay.ics`
- **Ambos países juntos:** `https://TU-USUARIO.github.io/calendario-economico/calendario_economico_ar_uy_outlook.ics`

Suscribite a Argentina y Uruguay por separado para tenerlos en **dos colores distintos**.

## 3. Suscribirse (vos y tus colegas)

**Google Calendar:** menú lateral → junto a *Otros calendarios* → **+** → **Desde una URL** → pegá la URL → Agregar. El color se cambia en los tres puntos del calendario.

**Outlook (web / nuevo):** Calendario → **Agregar calendario** → **Suscribirse desde la web** → pegá la URL → nombre y color → Importar.

**Apple Calendar:** Archivo → **Nueva suscripción de calendario** → pegá la URL.

Compartís las URLs con tus colegas y cada uno se suscribe. Cuando el feed cambia, todos lo ven actualizado (Google refresca cada ~8–24 h; Outlook similar).

## 4. Actualización automática

El workflow `.github/workflows/actualizar.yml` corre el **día 1 de cada mes** (y se puede correr a mano desde la pestaña **Actions**). Regenera los `.ics` con una **ventana móvil de ~13 meses** desde la fecha actual, así el calendario nunca se queda sin fechas. Las fechas confirmadas del calendario oficial están en el diccionario `OV` dentro de `generar_calendario.py`; para incorporar nuevos cronogramas oficiales, se agregan ahí y el robot publica el cambio solo.

## Generar localmente (opcional)

```bash
python generar_calendario.py                 # ambos países, con emojis
OUTLOOK=1 python generar_calendario.py        # versión sin emojis (Outlook)
OUTLOOK=1 PAIS=AR python generar_calendario.py
OUTLOOK=1 PAIS=UY python generar_calendario.py
```
