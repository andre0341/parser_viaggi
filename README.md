# parser_viaggi

Questo progetto contiene uno script Python per effettuare lo scraping delle offerte presenti su <https://offerte.caesartour.it/last-second.aspx> e salvarle in un database SQLite. 
È presente anche una piccola dashboard realizzata in Node.js che consente di filtrare e ordinare i risultati.

## Requisiti
- Python 3 con i pacchetti `requests` e `beautifulsoup4`.
- Node.js (per avviare la dashboard).

## Utilizzo
1. **Esecuzione dello scraper**
   ```bash
   python scraper.py
   ```
   Lo script crea (se non esiste) il database `db.sqlite` e inserisce le offerte recuperate.

2. **Avvio della dashboard**
   Dopo aver installato le dipendenze (`npm install`), avviare:
   ```bash
   npm start
   ```
   La dashboard sarà disponibile su <http://localhost:3000>.

La pagina consente di filtrare per Paese, formula e aeroporto, nonché di ordinare i risultati cliccando sull'intestazione delle colonne.
