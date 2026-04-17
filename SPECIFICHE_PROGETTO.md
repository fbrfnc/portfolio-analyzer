**✅ SPECIFICHE TECNICO-FUNZIONALI DEL PROGETTO**  
**Portfolio Analyzer MVP**  
**Versione 1.0**  
**Data:** 17 aprile 2026  
**Autore:** Grok (Consulente Programmazione & Analisi Finanziaria)  
**Formato:** Salva questo testo come file **`SPECIFICHE_PROGETTO.md`** nella root del repository.

---

### 1. Introduzione e Scopo

**Nome progetto:** Portfolio Analyzer  
**Obiettivo:** Sviluppare un’applicazione **desktop locale** (standalone) per l’analisi e il monitoraggio di un portafoglio di investimento composto da **Azioni, ETF e Fondi comuni**.  

L’applicazione deve calcolare in modo **preciso e matematicamente rigoroso**:
- Valutazione corrente del portafoglio
- Metriche di **performance**
- Metriche di **rischio**
- Confronto con benchmark

**Vincoli principali dell’MVP** (priorità 0):
- Solo utente singolo (single-user)
- Aggiornamento **giornaliero** (end-of-day)
- Solo fonti dati **gratuite**
- Deploy **desktop locale** (no cloud)
- Stack: **Python 3.12 + Streamlit** (trasformato in eseguibile con PyInstaller)

---

### 2. Requisiti Funzionali – MVP (Priorità 0)

#### 2.1 Gestione del Portafoglio (CRUD)
- Creazione, modifica, eliminazione di **posizioni**
- Supporto multi-portafoglio (es. “Principale”, “Pensione”, “Speculativo”)
- Campi obbligatori per ogni posizione:
  - ISIN / Ticker
  - Nome strumento
  - Tipo asset (`Azione` | `ETF` | `Fondo`)
  - Quantità / Quote
  - Costo medio ponderato (o storico tranches)
  - Data/e di acquisto
  - Valuta di denominazione
  - Commissioni di acquisto (facoltative)
  - Categoria personalizzata (settore, regione, stile)

#### 2.2 Recupero Prezzi e Dati (Giornaliero)
- Prezzi di chiusura storici (minimo 10 anni)
- Prezzi end-of-day aggiornati quotidianamente
- Gestione automatica di **dividendi** e **split**
- Conversione multi-valuta con tassi ECB ufficiali
- Cache locale aggressivo (SQLite + pickle)

#### 2.3 Calcolo Metriche di Performance
- Total Return (con/senza reinvestimento dividendi)
- Time-Weighted Return (TWR)
- Money-Weighted Return (MWR / IRR)
- CAGR (Compound Annual Growth Rate)
- Rendimenti periodici: 1M, 3M, 6M, YTD, 1Y, 3Y, 5Y, Inception
- Performance cumulativa

#### 2.4 Calcolo Metriche di Rischio
- Volatilità annualizzata
- Sharpe Ratio (risk-free rate da ECB o valore fisso)
- Maximum Drawdown + durata recupero
- Beta vs benchmark
- Value at Risk (VaR parametrico 95%)

#### 2.5 Confronto con Benchmark
- Benchmark predefiniti: MSCI World, Euro Stoxx 50, S&P 500, indice personalizzato (es. 60/40)
- Excess Return, Tracking Error di base

---

### 3. Requisiti Non Funzionali (Priorità 0/1)

- **Usabilità:** Interfaccia intuitiva con dashboard, grafici interattivi (Plotly), tema chiaro/scuro
- **Manutenibilità:** Codice modulare, ben documentato, facile da estendere
- **Multi-valuta:** Gestione nativa (visualizzazione in EUR o valuta originale)
- **Prestazioni:** Ottimizzato per portafogli con centinaia di posizioni
- **Sicurezza/Privacy:** Tutti i dati restano sul PC dell’utente (GDPR-ready per futuri sviluppi)
- **Offline:** Funziona completamente offline dopo il primo aggiornamento giornaliero

---

### 4. Architettura Tecnica e Stack (Priorità 0)

| Componente          | Scelta definitiva                  | Motivazione |
|---------------------|------------------------------------|-------------|
| Linguaggio          | Python 3.12                        | Standard quantitative finance |
| UI / Dashboard      | Streamlit                          | Rapidità + grafici interattivi |
| Database            | SQLite (file unico)                | Desktop locale, zero configurazione |
| ORM                 | SQLAlchemy (opzionale) o sqlite3   | Flessibilità |
| Calcoli             | pandas, numpy, scipy               | Precisione numerica |
| Dati prezzi         | yfinance + ECB API                 | Gratuite |
| Grafici             | Plotly                             | Interattivi e belli |
| Packaging Desktop   | PyInstaller                        | Eseguibile .exe / bundle |
| Cache               | Pickle + SQLite                    | Velocità |

**Struttura cartelle progetto (da creare):**
```
portfolio-analyzer/
├── app/                  # Codice Streamlit
│   ├── main.py
│   ├── pages/
│   ├── core/             # calcoli, metriche
│   ├── data/             # fetch, cache
│   └── models/           # SQLAlchemy o dataclass
├── data/                 # database.sqlite, cache
├── requirements.txt
├── SPECIFICHE_PROGETTO.md   ← **questo file**
├── README.md
└── build/                # PyInstaller output
```

---

### 5. Modello Dati (Schema Database)

**Tabella `portfolios`**  
- id (PK)  
- name  
- currency (default EUR)

**Tabella `positions`**  
- id (PK)  
- portfolio_id (FK)  
- isin_ticker  
- name  
- asset_type  
- quantity  
- cost_basis (costo medio)  
- purchase_dates (JSON o tabella separata)  
- currency  
- commissions  
- category

**Tabella `price_history`** (cache)  
- ticker  
- date  
- close_price  
- dividend  
- currency

**Tabella `exchange_rates`** (ECB)  
- date  
- from_currency  
- to_currency  
- rate

---

### 6. Metriche – Formule Matematiche (riferimento Dispense Palestini)

**Performance**  
\[
\text{Total Return} = \frac{V_t - V_0 + D}{V_0}
\]  
\[
\text{CAGR} = \left( \frac{V_t}{V_0} \right)^{1/n} - 1
\]  
TWR e MWR secondo definizione standard (cfr. Capitolo 5 Dispense).

**Rischio**  
\[
\sigma = \sqrt{\frac{1}{N-1} \sum (r_i - \bar{r})^2} \quad \text{(annualizzata × √252)}
\]  
\[
\text{Sharpe} = \frac{R_p - R_f}{\sigma_p}
\]  
\[
\text{Max Drawdown} = \max_{t} \left( \frac{P_t - \max_{i\leq t} P_i}{\max_{i\leq t} P_i} \right)
\]

---

### 7. Fonti Dati Gratuite & Limitazioni Note (2026)

- **yfinance**: prezzi azioni/ETF + dividendi
- **ECB API**: tassi di cambio ufficiali
- **Fondi comuni**: inserimento manuale NAV o CSV (limitazione nota)
- **Cache**: 1 giorno per prezzi, 30 giorni per storici
- **Rate limit**: rispettati con sleep e cache

---

### 8. Piano di Sviluppo MVP (4 Sprint)

**Sprint 0** – Setup (1-2 gg)  
**Sprint 1** – Gestione portafoglio + SQLite (3-4 gg)  
**Sprint 2** – Data fetch yfinance + ECB + cache (4 gg)  
**Sprint 3** – Metriche performance/rischio + dashboard (5 gg)  
**Sprint 4** – Grafici, benchmark, PyInstaller packaging (3-4 gg)

**Durata totale stimata:** 3-4 settimane (lavorando insieme).

