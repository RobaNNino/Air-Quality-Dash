# Air Quality Dash

Dashboard minimale per visualizzare le stazioni e le metriche della qualità dell'aria, con backend Flask come proxy/normalizzatore e frontend Nuxt 4 con UI in stile iOS e grafici.

## Panoramica

- Backend (cartella `backend/`):
  - Espone due endpoint `/api` che proxyano l'API upstream `zeroc.green`.
  - Arricchisce il dettaglio stazione calcolando la media ponderata degli ultimi 7 giorni per ogni metrica.
- Frontend (cartella `frontend/`):
  - SPA Nuxt 4 (SSR disabilitato) che consuma gli endpoint locali.
  - Pagina lista stazioni con card in stile iOS e info aggiuntive (indirizzo, coordinate, metriche).
  - Pagina dettaglio con toggle tra tabella e grafici lineari (min/avg/max) per ogni metrica.

## Requisiti

- Python 3.10+
- Node.js 18+ e npm

## Avvio rapido

### 1) Backend

```powershell
cd "backend"
python -m venv .venv 
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Avvia su http://127.0.0.1:5000
python app.py
```

### 2) Frontend

```powershell
cd "frontend"
# opzionale: cambia la base API, default: http://127.0.0.1:5000/api
$env:API_BASE = "http://127.0.0.1:5000/api"
npm ci
npm run dev
```

Nota: `nuxt.config.ts` legge `process.env.API_BASE` e, se non impostata, usa `http://127.0.0.1:5000/api`.

---

## Versioni utilizzate

Backend (requirements.txt):

- Python: 3.10+ (consigliato)
- Flask: 2.3.3
- flask-cors: 3.0.10
- requests: 2.31.0

Frontend (package.json e output build):

- Node.js: 18+ (consigliato)
- Nuxt: 4.2.0
- Vue: 3.5.22
- Vue Router: 4.6.3
- Vite: 7.1.12 (da output build)
- Nitro: 2.12.9 (da output build)
- chart.js: 4.4.7
- vue-chartjs: 5.3.1

Nota: le versioni frontend sono allineate a `package.json` e ai numeri riportati nella build di produzione.

## Backend: come funziona, passo per passo

File: `backend/app.py`

- Import e configurazione:
  - `Flask`, `jsonify`, `CORS` per server e CORS.
  - `requests` per proxy verso upstream.
  - `compute_weighted_average` dal modulo `calculations`.
- `BASE_URL = "https://api.zeroc.green/v1/"` definisce la sorgente upstream.
- `GET /api/stations`:
  - Effettua `requests.get(BASE_URL + "stations/")` con timeout.
  - Propaga la risposta JSON oppure un errore 502 in caso di problemi.
- `GET /api/stations/<station_id>`:
  - Richiede i dati di una singola stazione.
  - Normalizza `metrics` in una struttura iterabile (gestisce sia lista che dict).
  - Garantisce che ogni metrica abbia `daily` (usa `data_points` come fallback).
  - Calcola `weighted_average_last7` con la funzione di utilità e la inserisce in ogni metrica.
  - Restituisce il JSON arricchito.
- `app.run(debug=True, port=5000)` avvia il server in locale.

File: `backend/calculations.py`

Funzione chiave, commentata riga per riga:

```python
def compute_weighted_average(days):
    """
    Calcola la media ponderata degli ultimi 7 giorni
    usando average e sample_size.
    Esclude i giorni con sample_size == 0 o average == None.
    """
    if not days:
        return None  # nessun dato

    # prendiamo solo gli ultimi 7 giorni (o meno se non ci sono)
    last7 = days[-7:] if len(days) >= 7 else days

    total_weighted = 0
    total_samples = 0

    for d in last7:
        avg = d.get("average")
        samples = d.get("sample_size", 0)
        if samples > 0 and avg is not None:
            total_weighted += avg * samples  # accumula media * peso
            total_samples += samples         # accumula peso (n. campioni)

    if total_samples == 0:
        return None  # evita divisione per 0

    return total_weighted / total_samples   # media ponderata
```

`backend/requirements.txt` blocca le versioni: `flask`, `requests`, `flask-cors`.

---

## Frontend: struttura e flusso

Configurazione: `frontend/nuxt.config.ts`

- `ssr: false`: app SPA.
- `runtimeConfig.public.apiBase`: parametro di configurazione della base URL dell'API, di default `http://127.0.0.1:5000/api`, sovrascrivibile via `API_BASE`.

### Dipendenze principali (`frontend/package.json`)

- `nuxt`, `vue`, `vue-router`: stack Nuxt 4.
- `chart.js` + `vue-chartjs`: grafici lineari responsive nella pagina dettaglio.

### Stili globali iOS-like (`frontend/app/app.vue`)

- Usa font di sistema (`-apple-system`, ecc.) e colori sobri.
- Introduce classi riutilizzabili:
  - `.container`: larghezza max e padding.
  - `.card`: superfici bianche con bordo e ombra leggerissima.
  - `.row`: layout flessibile a griglia fluida.
  - `.chip`: pilloline informative.
  - `.segmented`: controllo "segmentato" iOS per il toggle Tabella/Grafici.
  - `.muted`: testo secondario.

### Pagina lista stazioni (`frontend/app/pages/index.vue`)

- Dati:
  - `useFetch('/stations')` per ottenere la lista.
  - `stations` come computed.
  - Helper robusti per address/city/coords che leggono da più campi possibili (es. `station.address`, `station.location.address`, ecc.).
- UI:
  - Header con titolo e sottotitolo.
  - Griglia di card, una per stazione.
  - Ogni card mostra:
    - Nome stazione e indirizzo (se disponibile) o città.
    - Chip con numero metriche, coordinate e quota (se presenti).
    - Link rapido a dettaglio (chevron + link in basso).
- Stili:
  - Niente inline CSS: tutte le regole sono in `<style scoped>` con classi come `.station-card`, `.card-top`, `.station-name`, `.chip-row`, ecc.

### Pagina dettaglio stazione (`frontend/app/pages/station/[id].vue`)

- Dati:
  - `useFetch('/stations/:id')` per ottenere il dettaglio.
  - `metrics` computed con fallback a array vuoto.
- Toggle vista:
  - `view` in `ref('table')` con controllo `.segmented` (Tabella/Grafici).
- Grafici:
  - Registrazione moduli Chart.js (`LineElement`, `CategoryScale`, ecc.).
  - `buildChartData(metric)` produce labels (date) e dataset per `min`, `average`, `max` con colori coerenti iOS.
  - `baseChartOptions` imposta tooltip, legenda, grid leggera, interazione non-intersect.
  - Ogni metrica viene resa in una card; se `view==='charts'` mostra `<Line />` responsivo, altrimenti la tabella.
- Tabella:
  - Colonne: Data, Min, Avg, Max, Campioni.
  - Layout responsive con `.table-wrap` e `.data-table`.
- Stili:
  - Inline CSS rimossi; tutto in `<style scoped>` con classi come `.detail-header`, `.metric-card`, `.data-table`, `.chart-wrap`.

---

## Cosa è stato fatto (cronologia interventi)

1. Backend
   - Creati endpoint `/api/stations` e `/api/stations/:id` (proxy + arricchimento).
   - Implementata la funzione `compute_weighted_average` e agganciata per ogni metrica nel dettaglio.
2. Frontend
   - Configurata `runtimeConfig.public.apiBase` in `nuxt.config.ts`.
   - Pagina `index.vue` per la lista:
     - Fetch, helpers per indirizzo/città/coordinate.
     - UI a card in stile iOS; chip informative; link a dettaglio.
     - Spostati gli stili dentro `<style scoped>` (no inline CSS).
   - Pagina `station/[id].vue` per il dettaglio:
     - Fetch del dettaglio e visualizzazione metriche.
     - Aggiunto toggle segmentato tra Tabella e Grafici.
     - Integrati `chart.js` e `vue-chartjs` per i grafici lineari min/avg/max.
     - Spostati gli stili dentro `<style scoped>` (no inline CSS).
   - Stili globali in `app.vue` per look & feel iOS (font, card, chip, segmented).
3. Build & verifica
   - Installate le dipendenze frontend.
   - Build di produzione per validare la compilazione.

---
