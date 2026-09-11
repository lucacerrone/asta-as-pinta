# Asta AS Pinta: guida completa ad architettura, dati e sviluppo

Versione app 2.1. Base dati 10/09/2026, integrazione Juventus/Lazio 11/09/2026. Questo documento serve a capire, usare e modificare il tool anche senza chi l'ha costruito, per esempio incollandolo in ChatGPT insieme ai file del repo.

---

## 1. Contesto: lega e obiettivo del tool

**Lega FantaEnel 1X2**, piattaforma Leghe Fantacalcio, modalità **Mantra**, stagione 2026/27.

- **14 squadre.** La nostra è **AS Pinta** (io + Ric). Le altre: chill curre, S.S. Longobarda, Al-Chaos-Ahli, AC OMMODITY, Pro Stata, Real Skënderbeu, Space Invaders, AS Emazz, NewRock, Fc Afragolese, Fight Club, Big Tasty FC, Fun Cool FC.
- **Asta random totale** (i nomi escono a caso da tutto il listone, niente chiamata), **500 crediti** a squadra, niente giocatori di Serie B.
- **Rosa:** portieri 2-4, movimento 23-26, totale 25-30.
- **Bonus/malus:**
  - gol +3 (uguale per tutti i ruoli), rigore segnato +3, rigore sbagliato -3;
  - assist +1 (gold +1,5, soft +0,5), rigore parato +3;
  - porta inviolata +1, gol subito -1;
  - autogol -2, espulsione -1, ammonizione -0,5;
  - gol vittoria, gol pareggio e player of the match valgono 0.
- **Formula:** scontri diretti 1X2, fasce da 6 punti, "limita pareggio" a 4 punti. Voti Fantacalcio.
- **Sostituzioni BASIC:** conta l'ordine di panchina; il sistema prova prima il modulo base, poi altri moduli, solo alla fine sostituzioni adattate con malus.
- **Calendario:** la lega parte dalla **5ª giornata di Serie A**. Prima sfida: AS Pinta - Fight Club.
- **Scelta nostra:** i giocatori di **Juventus** e **Lazio** sono inclusi nel listone e nell’asta, ma AS Pinta li considera di default **“ultima spiaggia”** (1 credito), salvo MUST manuale.

**Obiettivo del tool:** durante l'asta random, dato il nome appena uscito, dire subito **se prenderlo e fino a quanto**. Tiene conto di valore stimato, tetti, crediti rimasti, posti obbligatori da riempire, riserve per i MUST e rilancio massimo possibile dei rivali.

---

## 2. Struttura del repository

```
asta-as-pinta/
├── index.html            app completa (HTML + CSS + JS, nessuna libreria esterna)
├── README.md             istruzioni rapide di messa online
├── .nojekyll             dice a GitHub Pages di servire i file così come sono
└── data/
    ├── players.json      listone (507 giocatori), sola lettura
    ├── shortlist.json    obiettivi Piano A/B/C
    └── config.json       squadre, regole, prezzi, impostazioni iniziali, MUST, da evitare
```

Sul branch **`stato`**, creato automaticamente dall'app: `data/state.json` con lo stato dell'asta.

**Hosting:** GitHub Pages dal branch `main`, cartella root, URL `https://UTENTE.github.io/asta-as-pinta/`.

**Nessun backend.** Il browser legge i JSON statici da Pages, salva lo stato in `localStorage` e, se c'è un token, lo scrive su GitHub tramite l'API REST.

```
 iPad / Safari
 ┌─────────────────────────────────────────────┐
 │ index.html                                  │
 │   fetch data/*.json ◄──── GitHub Pages (main)│
 │   localStorage  (stato + copia dati + token) │
 │   fetch api.github.com ──► branch "stato"    │
 │                            data/state.json   │
 └─────────────────────────────────────────────┘
 Copilot / ChatGPT (fuori dall'app): screenshot → righe di testo → incolla nella scheda "Da foto"
```

---

## 3. Schemi dei dati

### 3.1 `data/players.json`
È un array di oggetti, ordinato per punteggio decrescente.

| Campo | Tipo | Significato | Esempio |
|---|---|---|---|
| `n` | string | Nome come nel listone Fantacalcio (cognome + iniziale se serve) | `"Martinez L."` |
| `t` | string | Squadra Serie A (nome esteso) | `"Inter"` |
| `v` | 0/1 | 1 = squadra verificata dalle fonti; 0 = dedotta o da verificare | `1` |
| `r` | string | Ruoli Mantra separati da `;` in ordine Por, Dc, B, Dd, Ds, E, M, C, W, T, A, Pc | `"M;C"` |
| `tr` | string | Ruolo "top" (quello con la fascia migliore) | `"M"` |
| `ft` | string | Fascia SOS Fanta nel ruolo top | `"SOTTO AI SEMITOP"` |
| `fr` | string | Fasce per ogni ruolo | `"M: SOTTO AI SEMITOP \| C: FASCIA MEDIA"` |
| `s` | string | Titolarità dall'XI tipo | `"Titolare"`, `"Titolare (ballott. con Pasalic)"`, `"Alternativa a Scamacca"`, `"Non nel XI tipo"`, `"n.d."` |
| `rg` | string | Ordine rigoristi | `"1°"`, `"2°"`, `"3°"`, `""` |
| `pz` | string | Batte calci piazzati | `"Sì"` o `""` |
| `i` | string | Infortunio + impatto sulla lega | `"Stiramento (in dubbio 6ª). Rischia le prime 2 giornate di lega"` |
| `sc` | int | Punteggio 0-100 | `86` |
| `c` | string | Consiglio base | `"OBIETTIVO"` |
| `f` | float | Fattore sul tetto | `1.1` |
| `fv` | int | FVM Mantra fantacalcio.it (valore su 1000 crediti) o stima | `32` |
| `fe` | 0/1 | 1 = FVM stimato dalla fascia | `0` |
| `no` | string | Note e consigli | `"M/C Frosinone: 1° rigorista..."` |

### 3.2 `data/shortlist.json`
Array di terne `[reparto, piano, nome]`, per esempio `["Punte - Pc", "A (tetto!)", "Martinez L."]`. I nomi devono esistere in `players.json`.

### 3.3 `data/config.json`
```json
{
  "noi": "AS Pinta",
  "squadre": ["AS Pinta", "chill curre", "..."],
  "regole": {"porMin": 2, "porMax": 4, "movMin": 23, "movMax": 26, "rosaMax": 30},
  "impostazioni": {"budget": 500, "tetto": 25, "stile": "Normale", "riserva": 30, "target": 27},
  "prezzi": {"sogliaBig": 150, "sogliaMedi": 40, "moltBig": 1.0, "moltMedi": 1.15, "moltBassi": 1.3, "extraMust": 1.3},
  "minimiRuolo": {"Por": 2, "Dc": 5, "B": 0, "Dd": 2, "Ds": 2, "E": 2, "M": 3, "C": 3, "W": 2, "T": 2, "A": 2, "Pc": 3},
  "must": [{"n": "Dybala", "max": 80, "why": "motivo"}],
  "evita": ["Varela G."],
  "github": {"repo": "asta-as-pinta", "branch": "stato", "file": "data/state.json"}
}
```

- **Impostazioni:** `tetto` è una percentuale del budget; `stile` può essere `Prudente`, `Normale` o `Aggressivo`; `riserva` sono i crediti extra da tenere per il finale.
- **Lettura:** `config.json` è riletto a ogni avvio.
- **MUST ed evita:** entrano nello stato solo alla prima apertura o col pulsante *Obiettivi > Importa MUST e da evitare da config.json*.

### 3.4 Stato (`localStorage["astaPinta.state.v2"]` e `data/state.json` sul branch `stato`)
```json
{
  "version": 2,
  "updatedAt": 1789140000000,
  "set": {"budget": 500, "tetto": 25, "stile": "Normale", "riserva": 30, "target": 27},
  "mine": [{"n": "Calò", "p": 21}, {"n": "Nome fuori lista", "p": 3, "por": true}],
  "asg": {"Calhanoglu": {"t": "Fight Club", "p": 131, "s": 1}},
  "riv": {"chill curre": {"c": 412, "g": 5, "p": 2}},
  "must": [{"n": "Dybala", "max": 0, "why": ""}],
  "black": ["Varela G."],
  "upd": "21:04",
  "log": [{"ts": 1789140000000, "a": "noi", "n": "Calò", "t": "AS Pinta", "p": 21}]
}
```

| Campo | Significato |
|---|---|
| `updatedAt` | Timestamp dell'ultima modifica; decide chi vince tra dispositivo e GitHub |
| `mine` | Nostri acquisti. `por: true` solo per nomi fuori listone |
| `asg` | Giocatori andati ad altri. `t` squadra (può essere vuota), `p` prezzo (può essere vuoto), `s: 1` se i crediti sono già stati scalati al rivale |
| `riv` | Per ogni rivale: crediti `c`, giocatori `g`, portieri `p` |
| `must` | MUST; `max: 0` significa "automatico" |
| `black` | Da evitare |
| `upd` | Ora dell'ultimo aggiornamento dei rivali |
| `log` | Storico azioni (massimo 1000 righe) |

Altre chiavi `localStorage`: `astaPinta.github.v1` (utente, repo, branch, token, file) e `astaPinta.data.v1` (copia di players, config e shortlist per l'uso offline).

---

## 4. Come sono stati costruiti i dati (players.json)

**Fonti:** dataset base letto il 10/09/2026; Juventus/Lazio integrate e verificate l’11/09/2026:
- SOS Fanta, guida Mantra 2026/27 ruolo per ruolo: fasce e ruoli Mantra;
- fantacalcio.it:
  - quotazioni e FVM Mantra;
  - probabili formazioni (XI tipo, ballottaggi, rigoristi, piazzati);
  - trasferimenti ufficiali;
  - fantaschede dei nuovi arrivi;
  - articolo sul budget;
- SOS Fanta: tabella indisponibili (09/09 23:30), news infortuni, "sei sorprese dopo la 3ª giornata";
- Forum Gruppo Esperti (estratti pubblici sul Mantra 2026/27).

**Ruoli.** Un giocatore ha tutti i ruoli in cui compare nella guida SOS; per ogni ruolo resta la fascia migliore.

**Punti per fascia:**

| Fascia | Punti | Fascia | Punti |
|---|---|---|---|
| SUPER TOP | 100 | JOLLY 2ª FASCIA | 40 |
| TOP | 90 | INFORTUNATI | 38 |
| SEMITOP | 80 | LOW COST 1ª FASCIA | 35 |
| SOTTO AI SEMITOP | 72 | RUOLO SECONDARIO 1ª FASCIA | 33 |
| FASCIA ALTA | 65 | LOW COST 2ª FASCIA | 28 |
| JOLLY 1ª FASCIA | 58 | RUOLO SECONDARIO 2ª FASCIA | 26 |
| POSSIBILI SORPRESE | 55 | LEGHE NUMEROSE | 25 |
| FASCIA MEDIA | 50 | JOLLY 3ª FASCIA | 22 |
| SOPRA AI LOW COST | 45 | JOLLY 4ª FASCIA | 15 |
| SCOMMESSE | 42 | A RISCHIO | 10 |
| | | DA EVITARE | 5 |

**Punteggio `sc`.** Si parte dai punti della fascia migliore e si aggiunge:

| Voce | Effetto |
|---|---|
| Titolare | +5 |
| Titolare in ballottaggio | +2 |
| Alternativa | -6 |
| Non nel XI tipo | -10 |
| Rigorista | 1° +5, 2° +3, 3° +1 |
| Calci piazzati | +2 |
| Due ruoli | +2 |
| Tre ruoli o più | +3 |
| Infortunio | secondo le giornate di lega a rischio (vedi sotto) |

Il risultato è limitato tra 0 e 100.

**Infortunio.**
- **Giornate di lega a rischio:** `miss = max(0, giornata_rientro - 4)`, perché "in dubbio per la 6ª" significa che può saltare la 5ª e la 6ª.
- **Stime usate:** McTominay, Spence e Volpato rientro alla 8ª, Solet alla 6ª, Dimarco alla 4ª.
- **Penalità:**

| Giornate a rischio | Penalità |
|---|---|
| 0 | 0 |
| 1 | -3 |
| 2 | -8 |
| 3-5 | -15 |
| 6 o più | -35 |

**Consiglio `c` e fattore `f`.** Le regole si applicano nell'ordine; vale la prima che corrisponde.

| Condizione | Consiglio | Fattore |
|---|---|---|
| miss ≥ 6 | EVITA (infortunio lungo) | 0,5 |
| Fascia ≤ 10 punti | EVITA | 0,6 |
| miss ≥ 2 e fascia ≥ 65 punti | OCCASIONE (infortunato) | 0,8 con miss = 2; 0,7 con miss 3-5 |
| Punteggio ≥ 90 | TOP - vale lo sforzo | 1,10 |
| Punteggio ≥ 76 | OBIETTIVO | 1,10 |
| Punteggio ≥ 62 | BUONO / VALUE | 1,00 |
| Punteggio ≥ 48 | SCOMMESSA / 2° SLOT | 1,00 |
| Punteggio ≥ 32 | LOW COST | 0,90 |
| Altrimenti | ULTIMI CREDITI | 0,80 |

**Correzioni successive:**
- **Alternative:** fattore ×0,85.
- **Hype**, con etichetta " - attenzione hype":

| Giocatore | Fattore |
|---|---|
| Esposito F.P., Cissè A., Castro S. | ×0,7 |
| Douvikas, Varela G. | ×0,75 |
| Milla, Piccoli | ×0,8 |
| Raimondo, Kvernadze, Malen | ×0,9 |

**FVM stimato** (per chi non era nella tabella quotazioni).
- **Valori per fascia:**

| Fascia | FVM stimato |
|---|---|
| SUPER TOP, TOP | 15 |
| SEMITOP | 12 |
| SOTTO AI SEMITOP | 10 |
| FASCIA ALTA | 9 |
| JOLLY 1ª | 7 |
| SORPRESE, MEDIA | 6 |
| SOPRA AI LOW COST | 5 |
| SCOMMESSE, JOLLY 2ª | 4 |
| INFORTUNATI, LOW COST 1ª, RUOLO SECONDARIO 1ª | 3 |
| LOW COST 2ª, RUOLO SECONDARIO 2ª, LEGHE NUMEROSE, JOLLY 3ª | 2 |
| JOLLY 4ª, A RISCHIO, DA EVITARE | 1 |

- **Correzione finale:** `fv = max(stima, round((sc - 40) / 2))`.

**Taratura prezzi.** In lega girano 14 × 500 = 7.000 crediti. I 378 giocatori più cari valgono circa 6.080 crediti a FVM puro. Con i moltiplicatori 1,00 (FVM ≥ 150), 1,15 (40-149) e 1,30 (< 40) il totale stimato arriva a circa 7.070.

**Come modificare i dati senza lo script originale:** apri `players.json` e cambia i campi del giocatore. Serve JSON valido: controllalo per esempio chiedendo a ChatGPT di validarlo. Per aggiungere un giocatore copia un oggetto esistente e cambia i valori; `fv` e `f` bastano per avere prezzi sensati.

---

## 5. Calcoli nell'app (index.html)

```text
mult(fv)    = fv ≥ sogliaBig ? moltBig : fv ≥ sogliaMedi ? moltMedi : moltBassi
market(p)   = max(1, round(p.fv / 1000 × budget × mult(p.fv)))
aggr        = Prudente 0,9 | Normale 1,0 | Aggressivo 1,1
baseMax(p)  = min(round(tetto% × budget), max(1, round(market × p.f × aggr)))
maxFor(p)   = MUST ? (max > 0 ? max : max(round(market × extraMust), baseMax)) : baseMax
consOf(p)   = MUST → "MUST" | in evita → "EVITA (scelta nostra)" | altrimenti p.c
```

**Situazione della nostra squadra: `me()`**
```text
spent = somma prezzi mine;  rem = budget - spent
por = portieri in mine (ruolo top "Por" o flag por);  mov = totale - por
porMiss = max(0, porMin - por);  movMiss = max(0, movMin - mov)
tecPor = (por ≥ porMax o tot ≥ rosaMax) ? 0 : max(0, rem - (max(0, porMiss-1) + movMiss))
tecMov = (mov ≥ movMax o tot ≥ rosaMax) ? 0 : max(0, rem - (porMiss + max(0, movMiss-1)))
mustRes = somma per i MUST non presi e non andati di (max > 0 ? max : round(market × extraMust))
finRes  = movMiss ≤ 3 ? 0 : min(riserva, max(0, rem - (porMiss + movMiss)))
consPor = max(0, tecPor - mustRes - finRes);  consMov = max(0, tecMov - mustRes - finRes)
```
"Tecnica" è il massimo possibile lasciando 1 credito per ogni posto obbligatorio; "consigliata" toglie anche le riserve.

**Rivali: `rivMax(r, portiere)`.** Stessa logica, con r.c crediti, r.g giocatori, r.p portieri e mov = g - p. `topRival()` restituisce il rivale con il rilancio più alto.

**Verdetto: `verdict(p)`**, in ordine di precedenza:

| Condizione | Verdetto | Colore |
|---|---|---|
| In `mine` | "Già nostro" | blu |
| In `asg` | "Andato a X" | grigio |
| Consiglio che inizia con EVITA | "Lascia" | rosso |
| Offerta disponibile ≤ 0 | "Non puoi" | rosso |
| MUST | "MUST: prendilo", fino a `min(maxFor, offerta)` | viola |
| TOP, OBIETTIVO o BUONO | "Prendi", fino a `min(maxFor, consPor/consMov)` | verde |
| OCCASIONE | "Occasione, solo a sconto" | ambra |
| Altro | "Solo se costa poco" | ambra |

- **Offerta per un MUST:** `max(0, tecnica - finRes - (mustRes - riserva del MUST stesso))`.
- **Suggerimenti (tip):**
  - se il rivale più ricco arriva a v < limite: "basta offrire v+1";
  - se il limite è dato dai nostri crediti, lo dice;
  - se il mercato supera il tetto di oltre il 30%: "probabilmente andrà oltre il tuo tetto".

---

## 6. Architettura del codice (index.html)

JavaScript vanilla, tutto in un unico `<script>`. Il rendering usa template string e `innerHTML`; gli eventi sono delegati sul `document` tramite attributi `data-*`.

| Blocco | Funzioni / oggetti | Ruolo |
|---|---|---|
| Globali | `APP_VERSION, ROLES, P, SHORT, CFG, TEAMS, NOI, RIVALS, RULES, PRICE, MINS, byName` | Riempiti da `init()` |
| Testo e ricerca | `norm, init, esc, searchPlayers, matchPlayer, matchTeam` | Normalizzazione (accenti, apostrofi), indici `_n _main _init _t`, ricerca, match fuzzy per l'import |
| Persistenza | `ls, defaults, merge, loadLocal, persist, logEvent, enc/dec, utf8b64/b64utf8` | Stato in `localStorage`, backup in base64 |
| GitHub | `gh.cfg, ok, base, req, explain, ensureBranch, getState, putState` | Chiamate REST |
| Sync | `sync.schedule, sync.run`, `connectAndPull`, `statusInfo`, `updateStatus` | Debounce, retry, allineamento, pallino di stato |
| Calcoli | `mult, aggr, market, baseMax, mustOf, maxFor, consOf, mineOf, isPor, resOf, me, rivMax, topRival, verdict` | Vedi sezione 5 |
| UI | `render, miniTag, viewCerca, resultsHTML, card, viewRosa, viewRivali, viewImporta, parseImport, applyImport, viewObiettivi, viewImpostazioni, copyText, toast, commit` | Schermate |
| Avvio | `fatal, fetchJSON, boot`, listener `visibilitychange` e `online` | Caricamento dati e sync iniziale |

**Flusso di una modifica:** click → handler → cambia `S` → `commit(msg)` → `persist()` (aggiorna `updatedAt`, salva in localStorage, `sync.schedule()`) → `render()` → toast.

**Ricerca:** durante la digitazione si aggiorna solo `#res`, per non far perdere la tastiera su iOS.

**Azioni `data-*`:**

| Attributo | Azione |
|---|---|
| `data-tab` | Cambia scheda (anche il pallino di stato porta a Impostazioni) |
| `data-open` | Apre la scheda giocatore |
| `data-back` | Nuova ricerca |
| `data-buy` | Preso da noi (prezzo da `#price`) |
| `data-other` | Preso da altri (squadra da `#team`, prezzo facoltativo; scala i crediti se entrambi presenti) |
| `data-undo` | Annulla assegnazione (ripristina i crediti del rivale se `s: 1`) |
| `data-must` / `data-black` | Aggiunge o toglie dai MUST / dagli evita |
| `data-mustmax`, `data-mustdel`, `data-blackdel` | Gestione liste in Obiettivi |
| `data-seedcfg` | Importa MUST ed evita da config.json |
| `data-role` | Filtro ruolo in "Migliori ancora liberi" |
| `data-del`, `data-editprice`, `data-addx` | Gestione rosa (anche giocatori fuori lista) |
| `data-riv` + `data-k` | Modifica crediti, giocatori o portieri di un rivale |
| `data-copy` | Copia prompt (squadre / giocatori) |
| `data-parse`, `data-apply`, `data-cancelimport` | Import da testo |
| `data-set` | Impostazioni (budget, tetto, riserva, stile) |
| `data-ghconnect`, `data-ghpush`, `data-ghpull`, `data-ghoff` | GitHub |
| `data-download`, `data-backup`, `data-restore`, `#restorefile`, `data-reset` | Backup e azzeramento (conferma con doppio tocco) |

**Schermate:** Cerca, Rosa (con storico azioni), Rivali, Da foto, Obiettivi, Impostazioni.

---

## 7. Sincronizzazione con GitHub

**Token.** Fine-grained personal access token, limitato al solo repo `asta-as-pinta`, con permesso **Contents: Read and write**. È salvato solo nel `localStorage` del dispositivo e non viene mai scritto nel repo.

**Endpoint** (header `Authorization: Bearer TOKEN`, `Accept: application/vnd.github+json`):

| Metodo | Endpoint | Uso |
|---|---|---|
| GET | `/repos/{owner}/{repo}` | Verifica accesso, legge `default_branch` |
| GET | `/repos/{owner}/{repo}/git/ref/heads/{branch}` | Il branch `stato` esiste? |
| POST | `/repos/{owner}/{repo}/git/refs` body `{ref:"refs/heads/stato", sha}` | Crea il branch dal default |
| GET | `/repos/{owner}/{repo}/contents/data/state.json?ref=stato` | Legge lo stato (`content` in base64, `sha`) |
| PUT | `/repos/{owner}/{repo}/contents/data/state.json` body `{message, content, branch:"stato", sha?}` | Scrive lo stato (crea o aggiorna) |

**Regole:**
1. **Salvataggio:** ogni modifica salva subito in locale e programma una PUT dopo 2,5 secondi. Modifiche ravvicinate producono un solo commit; se arriva una modifica mentre una PUT è in corso, ne parte un'altra alla fine.
2. **Conflitti:** con risposta 409/422 (sha non allineato) l'app rilegge lo sha e ripete la PUT. In caso di errore riprova ogni 15 secondi.
3. **All'avvio** con token (`connectAndPull`): crea il branch se manca e legge lo stato.
   - se su GitHub non c'è ancora, lo crea;
   - se quello remoto è più recente (`updatedAt`), lo carica;
   - se è più vecchio, lo sovrascrive.

   Vince l'ultima modifica.
4. **Quando l'app va in background** (`visibilitychange` hidden) o torna la rete (`online`): parte subito una PUT se c'è qualcosa da salvare.
5. **Pallino di stato:**

| Colore | Testo | Significato |
|---|---|---|
| Verde | "GitHub hh:mm" | Salvato su GitHub |
| Giallo | "Salvo su GitHub" | Salvataggio in corso |
| Rosso | "GitHub: errore" | Errore (dettaglio in Impostazioni) |
| Blu | "Salvato sul dispositivo" | Nessun token collegato |

"Non salvato!" compare se il localStorage non funziona, per esempio in navigazione privata.

**Perché un branch separato:** ogni commit su `main` farebbe ripartire la pubblicazione di GitHub Pages, e durante l'asta i commit sono centinaia.

**Limiti:** se due dispositivi modificano insieme, vince l'ultimo a salvare. Le chiamate autenticate all'API di GitHub hanno un limite orario ampio, lontano dalle poche centinaia di un'asta.

---

## 8. Import da screenshot (scheda "Da foto")

**Flusso:** screenshot dell'app d'asta → Copilot o ChatGPT con uno dei due prompt → righe di testo → incolla nel riquadro → "Leggi" → anteprima → "Applica".

**Formati accettati** (una riga per voce; separatori `;` `|` tabulazione, oppure virgola se non ce ne sono altri):
- `Squadra;crediti;giocatori;portieri` aggiorna un rivale (giocatori e portieri facoltativi);
- `Giocatore;Squadra;Prezzo` segna un'assegnazione (squadra e prezzo facoltativi).

Vengono ignorati puntini ed elenchi numerati, righe di intestazione, righe di separazione delle tabelle markdown e pipe iniziali o finali.

**Riconoscimento delle squadre (`matchTeam`):** nome identico, poi contenimento, poi una parola di almeno 4 lettere in comune.

**Riconoscimento dei giocatori (`matchPlayer`):**
- nome identico: 100 punti;
- tutti i token principali del listone presenti nel testo: 80, +10 se una parola extra comincia con l'iniziale (es. "Lautaro Martinez" → "Martinez L."), +5 se il numero di parole coincide.
- se i primi due candidati distano meno di 5 punti, il nome è "ambiguo" e non viene applicato.

I nomi non trovati o ambigui finiscono tra le "non riconosciute". Juventus e Lazio sono ora presenti nel listone.

**Opzione "Scala anche i crediti ai rivali":** sottrae prezzo e aggiunge un giocatore alla squadra indicata. Va lasciata spenta se nella stessa sessione importi anche i crediti delle squadre.

**Prompt nell'app:**
- **Squadre:** «Dallo screenshot dell'asta leggi, per ogni squadra, i crediti residui, il numero di giocatori in rosa e il numero di portieri (se non si vede lascia vuoto). Rispondi SOLO con righe nel formato Squadra;crediti;giocatori;portieri, una riga per squadra, senza intestazioni e senza altro testo. Squadre possibili: …»
- **Giocatori:** «Dallo screenshot dell'asta elenca i giocatori già assegnati. Rispondi SOLO con righe nel formato Giocatore;Squadra;Prezzo, una riga per giocatore, senza intestazioni e senza altro testo. Scrivi il nome del giocatore come appare nell'app. Squadre possibili: …»

---

## 9. Guida d'uso operativa

**Senza token:** l'app funziona lo stesso e salva sul dispositivo. Resiste alla chiusura di Safari e al riavvio, ma non alla navigazione privata, a "Cancella dati siti web" o al cambio di dispositivo.

**Con token (consigliato):** in più salva su GitHub, così puoi cambiare dispositivo e avere lo storico.

**Prima dell'asta**
1. Apri il link di Pages in Safari. Scegli una sola "porta": la scheda di Safari oppure l'icona in Home, perché l'icona può avere una memoria separata.
2. In Impostazioni collega GitHub e controlla che il pallino diventi verde.
3. In Obiettivi aggiungi i MUST con il prezzo massimo e gli eventuali "da evitare".
4. In Impostazioni controlla tetto (25% di default; 45% se volete una stella), stile e riserva.

**Durante l'asta**
1. **Esce un nome:** in Cerca scrivi 3-4 lettere e tocca il giocatore. Leggi verdetto e prezzo.
2. **Finita l'offerta:** "Preso da noi" col prezzo, oppure "Preso da altri" (squadra e prezzo se li sai). Se non ti interessa, puoi anche non segnare nulla.
3. **Ogni tanto** (dopo 60-80 assegnazioni, a metà asta e spesso nel finale): aggiorna i rivali, a mano o dalla scheda "Da foto".
4. **Controlla Rosa:** offerta massima, copertura ruoli, riserve.

**Emergenze**

| Situazione | Cosa fare |
|---|---|
| Pallino rosso | Tocca il pallino e leggi l'errore. Intanto i dati restano sul dispositivo |
| Pagina azzerata | Se collegato a GitHub, riapri e ricollega (carica da sola la versione più recente); altrimenti "Ripristina da codice/file" |
| iPad scarico | Apri il link su iPhone o PC, collega GitHub con lo stesso token: ritrovi tutto |
| App non parte | Aprila dal link di Pages, non come file. Se sei offline e l'avevi già aperta, usa la copia dei dati salvata |

---

## 10. Test

**In locale sul PC:**
```bash
cd asta-as-pinta
python -m http.server 8000
# apri http://localhost:8000
```
Aprire `index.html` con doppio clic non funziona: il browser blocca il caricamento dei file JSON locali.

**Checklist manuale:**
1. Cerca "calo" → Calò, verde, "Prendi fino a 23" (con impostazioni di default).
2. Preso da noi a 21 → in alto crediti 479. Chiudi e riapri la scheda: i crediti restano 479.
3. Collega GitHub → pallino verde; sul repo appare il branch `stato` con `data/state.json`.
4. Nuovo acquisto → dopo pochi secondi c'è un nuovo commit sul branch `stato`.
5. Da un secondo dispositivo, collegando GitHub, compaiono gli stessi acquisti.
6. Da foto: incolla `chill curre;412;5;2` e `Lautaro Martinez;NewRock;190` → Leggi → Applica → Rivali aggiornati e Martinez L. "andato".
7. Token sbagliato → pallino rosso e messaggio "Token non valido o scaduto".

**Test automatici usati in sviluppo:** Playwright con server locale e intercettazione di `https://api.github.com/**` tramite un finto GitHub in memoria (refs, contents con sha, 409 forzato). Scenari coperti: persistenza dopo chiusura, creazione branch e file, sync con debounce, conflitto e retry, nuovo dispositivo, avvio offline con dati in cache, token errato.

---

## 11. Backlog: upgrade possibili

Legenda: **Valore** per l'asta (A alto, M medio, B basso). **Sforzo** S piccolo (meno di 1 ora), M medio (2-4 ore), L grande (più di mezza giornata).

### 11.1 Funzionalità d'asta
| # | Idea | Valore | Sforzo | Come farla |
|---|---|---|---|---|
| ✅ F1 | **Annulla ultima azione** (pulsante sempre visibile) | A | S | Usare `S.log`: salvare nell'evento anche lo stato precedente dell'oggetto modificato e ripristinarlo |
| F2 | **Inflazione live**: prezzi stimati corretti in base a quanto si sta pagando davvero | A | S | `infl = somma prezzi pagati / somma market()` sui giocatori assegnati con prezzo (min 10 casi, limiti 0,8-1,4); `market` × infl; mostrare l'indice in Rosa |
| ✅ F3 | **Scarsità per ruolo**: quanti titolari buoni restano liberi rispetto a quanti ne servono alla lega | A | S | Per ogni ruolo: liberi con sc ≥ 60 e stato Titolare vs (squadre × minimo ruolo − già assegnati); badge "scarso" nel verdetto che alza leggermente il tetto |
| ✅ F4 | **Modalità asta a schermo intero**: verdetto enorme, due pulsanti grandi, nuova ricerca automatica | A | S | Variante di `card()` con CSS dedicato |
| F5 | **Rose dei rivali**: chi manca di portieri o Pc sarà aggressivo su quei ruoli | M | M | Da `asg` + `riv`: conteggi per squadra e ruolo; nel verdetto "3 squadre cercano ancora un portiere" |
| ✅ F6 | **Budget per reparto live** (profili Equilibrato / Stella / Bonus centrocampo come nell'Excel) | M | S | Percentuali in config; confronto con `mine` per area del ruolo top |
| F7 | **Costruttore di formazione e ordine panchina** per le sostituzioni BASIC | M | L | Tabella moduli Mantra con slot e ruoli ammessi; algoritmo greedy per i titolari; panchina ordinata per copertura dei ruoli |
| F8 | **Export rosa** (CSV / testo da incollare in chat) | M | S | Pulsante in Rosa che genera il CSV da `mine` + dati giocatore |
| F9 | **Vista per Ric in sola lettura** | M | S | Pagina che legge `state.json` sul branch `stato` ogni 30 secondi (con token di sola lettura, oppure dal file raw del repo pubblico, che però può arrivare con qualche minuto di ritardo) |
| ✅ F10 | **Alternative immediate**: nella scheda, i 3 migliori liberi dello stesso ruolo con prezzo | A | S | Filtro come "Migliori ancora liberi" ristretto a `tr` del giocatore |

### 11.2 Viste di monitoraggio
| # | Idea | Valore | Sforzo | Come farla |
|---|---|---|---|---|
| ✅ V1 | **Cruscotto**: % asta completata, % budget speso, inflazione, crediti medi per slot noi vs rivali | A | S | Formule già presenti nell'Excel (ritmo di spesa, potere d'acquisto) |
| ✅ V2 | **Classifica rivali per potere d'acquisto** (crediti per slot obbligatorio) | M | S | Ordinare la tabella Rivali per `c / slot obbligatori` |
| V3 | **Ultimi 10 assegnati** con prezzo pagato vs stimato (affari e strapagati) | M | S | Dal `log`; colori verde/rosso |
| V4 | **Mappa ruoli**: griglia con liberi per ruolo e fascia | M | M | Tabella ruoli × fasce con contatori cliccabili |
| V5 | **Grafico prezzi**: pagato vs stimato | B | M | SVG inline, niente librerie |

### 11.3 Insights
| # | Idea | Valore | Sforzo | Note |
|---|---|---|---|---|
| ✅ I1 | Allarme "rischio buco": quando in un ruolo obbligatorio restano meno titolari liberi di quanti te ne servono | A | S | Deriva da F3 |
| I2 | Stima della forza della rosa (somma punteggi dei titolari probabili) nostra vs rivali | M | M | Richiede che siano segnati anche i nomi degli altri |
| I3 | Aggiornamento news e infortuni dal web | M | L | Le fonti non espongono API aperte: servirebbe un servizio intermedio o un aggiornamento manuale di `players.json` |
| ✅ I4 | Suggerimento "chiudi ora": a fine asta, lista dei migliori a 1-3 crediti per completare i ruoli mancanti | A | S | Filtro per ruoli con "MANCA" e market ≤ 3 |

### 11.4 Grafica e immagini
| # | Idea | Valore | Sforzo | Note |
|---|---|---|---|---|
| G1 | **Colori e badge squadra** (sigla e colori sociali, niente immagini) | M | S | Mappa squadra → colori in config; badge CSS. Leggero e senza problemi di diritti |
| G2 | **Foto giocatori da internet** | B | M | Le foto dei siti fantacalcio e dei club sono protette e spesso bloccate se richiamate da altri siti. Wikimedia Commons ha licenze libere ma copre pochi giocatori ed è lenta. Durante un'asta rallenta e distrae: sconsigliata |
| G3 | Tema scuro per la sera e dimensione testo regolabile | M | S | Variabili CSS e `prefers-color-scheme` |

### 11.5 Screenshot e estrazione automatica dei nomi
| # | Opzione | Pro | Contro | Sforzo |
|---|---|---|---|---|
| S1 | **Testo attivo di iOS** (Live Text): nella foto/screenshot tieni premuto sul testo, Seleziona tutto, Copia, poi incolla in "Da foto" | Gratis, sul dispositivo, nessuna AI | Il testo arriva disordinato: serve un parser più tollerante (nomi e numeri su righe separate) | S-M (solo parser) |
| S2 | **Comando rapido iOS** "Estrai testo da immagine" su screenshot → appunti → apre l'app | Due tocchi, gratis | Stesso limite di ordine del testo; da configurare in Comandi | S |
| S3 | **OCR nel browser** (Tesseract.js) con caricamento immagine nell'app | Tutto nell'app, niente chiavi | Libreria pesante, lenta su iPad, precisione media su testo piccolo | M |
| S4 | **API vision di un LLM** chiamata dall'app (caricamento screenshot → JSON strutturato) | Precisione migliore, output già nel formato giusto | Serve una chiave API a pagamento, separata da ChatGPT Pro o Copilot; la chiave andrebbe tenuta solo sul dispositivo; costi per immagine | M |
| S5 | **Flusso attuale**: Copilot o ChatGPT con i prompt pronti | Zero sviluppo, già funzionante | Passaggi manuali (copia e incolla) | già fatto |

**Consiglio:** per stasera S5. Come upgrade successivo S1+S2 con parser tollerante (costo zero); S4 solo se serve davvero l'automazione completa.

### 11.6 Robustezza tecnica
| # | Idea | Valore | Sforzo |
|---|---|---|---|
| R1 | Service worker per l'avvio completamente offline (oggi si usano i dati salvati in localStorage) | M | M |
| R2 | Unione intelligente tra due dispositivi (per azioni del log invece di "vince l'ultimo") | B | L |
| R3 | Separare `index.html` in `app.js` e `style.css` per modifiche più facili | B | S |
| R4 | Validazione di config.json all'avvio con messaggi chiari (nomi MUST inesistenti, squadre duplicate) | M | S |

---

## 12. Come far continuare il lavoro a un'altra AI

1. **Carica nella chat:** questa guida, `index.html`, `data/config.json`, e se serve `data/players.json` (circa 120 KB).
2. **Usa un prompt di partenza come questo:**

> Sei uno sviluppatore front-end. Ti allego la guida dell'app "Asta AS Pinta" e i suoi file. È una web app statica (HTML/CSS/JS vanilla, nessuna libreria) su GitHub Pages, con stato in localStorage e sincronizzazione su GitHub tramite API REST sul branch "stato". Rispetta architettura, schemi dati e formule descritti nella guida. Voglio implementare: [descrivi l'upgrade, per esempio F2 "inflazione live"]. Restituiscimi solo le parti di codice da cambiare, con indicazione precisa di dove inserirle (nome della funzione esistente da modificare), senza riscrivere tutto il file. Non cambiare il formato di state.json se non strettamente necessario; se lo cambi, aggiorna merge() in modo compatibile con gli stati già salvati.

3. **Regole per modifiche sicure:**
   - dopo ogni modifica prova in locale con `python -m http.server` e la checklist della sezione 10;
   - un nuovo campo nello stato va aggiunto sia in `defaults()` sia in `merge()`;
   - una nuova azione UI va fatta con un pulsante `data-nuovaazione` e il suo ramo nel listener `click`;
   - non inserire mai il token nei file del repo;
   - per pubblicare: carica il file modificato su `main`; Pages si aggiorna in 1-2 minuti e l'app ricarica i dati a ogni apertura.

---

## 13. Limiti noti dei dati

- **Ruoli Mantra:** ricavati dalla guida SOS Fanta. Possono differire leggermente da quelli ufficiali della piattaforma.
- **Squadre da verificare:** alcuni giocatori di fascia bassa del dataset originario possono ancora avere `v: 0` o dati meno solidi. Juventus e Lazio sono state reintegrate usando le fonti ammesse.
- **FVM stimato:** per i giocatori con quotazione bassa il valore è stimato (`fe: 1`).
- **Aggiornamento:** base dati al 10/09/2026; integrazione Juventus/Lazio all’11/09/2026. Non c’è aggiornamento news automatico dal web.
- **Juve e Lazio:** sono nel listone. `config.json > evitaSquadre` le rende “ultima spiaggia” per AS Pinta, senza impedirne l’assegnazione ai rivali.


---

## 14. Versione 2.1 — stato del lavoro al 11/09/2026

Questa sezione prevale sulle descrizioni del backlog precedente quando c’è conflitto.

### Implementato nel batch prioritario

- **Juve/Lazio incluse:** `players.json` contiene 507 giocatori, con 30 Juventus e 30 Lazio. La regola AS Pinta è in `config.json` (`evitaSquadre`) e non rimuove i giocatori dall’asta. Un MUST manuale prevale.
- **“Perché” completo:** nessun record di `players.json` ha più la nota `no` vuota. Le note sono costruite esclusivamente dai campi/dati provenienti dalle due fonti già ammesse: SOS Fanta e Fantacalcio.it.
- **Responsive denso:** `.wrap` arriva a 1180 px. In landscape da 760 px in su, la ricerca mostra a sinistra i risultati e a destra la scheda aperta; su iPhone/portrait resta una sola colonna.
- **F10:** `alternatives(p)` mostra 3 liberi con lo stesso `tr`, escludendo già assegnati e giocatori evitati.
- **F1:** snapshot singolo in una chiave locale dedicata (`astaPinta.undo.v1` / `astaPinta.beta.undo.v1`). Il pulsante `↶ Annulla` ripristina l’ultima mutazione operativa e la sincronizza come nuovo stato.
- **Import screenshot:** le righe importate sono autoritative per quella voce. Possono correggere squadra/prezzo/assegnazione già registrati. Le righe crediti vengono applicate per ultime, quindi la fotografia dei rivali vince sugli aggiustamenti derivati dalle assegnazioni. L’assenza da uno screenshot non cancella dati.
- **Canale beta:** `beta.html` usa localStorage separato e forza `stato-beta`; condivide soltanto i JSON statici del branch pubblicato.
- **F4:** `auctionMode`; verdetto e pulsanti grandi, tab nascoste, focus alla ricerca dopo la registrazione dell’esito. Tasto `F4` disponibile su tastiera.
- **F3:** `scarcityFor()` confronta titolari buoni liberi (`sc >= 60`, `Titolare`) con gli slot minimi ancora non coperti nell’intera lega. A scarsità warning/critica il tetto base sale rispettivamente del 4%/8%. È una metrica indicativa perché i multiruolo contano su più ruoli.
- **I1:** `holeRisks()` segnala in Rosa i ruoli personali mancanti con disponibilità utile già stretta.
- **I4:** `closingCandidates()` propone fino a 8 liberi con `market <= 3` che coprono almeno un ruolo sotto minimo.
- **V1:** `auctionStats()` mostra avanzamento tracciato, quota di budget speso, inflazione osservata (solo informativa), crediti/slot nostri e medi rivali. Non modifica i prezzi automaticamente.
- **V2:** tabella Rivali ordinata per `crediti / slot obbligatori residui`.
- **F6:** `budgetStatus()` confronta spesa reale per macro-reparto con un profilo configurabile.

### Nota importante su F6

Il file Excel richiamato nel vecchio backlog non era tra i materiali ricevuti. Per non bloccare la funzione, `config.json` contiene tre **preset operativi provvisori e modificabili**:

| Profilo | Por | Difesa | Centrocampo | Trequarti | Attacco |
|---|---:|---:|---:|---:|---:|
| Equilibrato | 5% | 20% | 25% | 20% | 30% |
| Stella | 5% | 16% | 19% | 15% | 45% |
| Bonus centrocampo | 5% | 18% | 32% | 20% | 25% |

Questi numeri **non sono stati ricostruiti dall’Excel**. Se si recuperano i valori originari, basta cambiare `budgetReparti` in `config.json` senza toccare il codice.

### Cose volutamente non implementate in questo batch

Restano in fondo/priorità successiva secondo le indicazioni ricevute: **V5, G1, F7, V4, F9, G3**. **F2/V3** non sono stati attivati perché una sequenza di screenshot a salti non garantisce una cronologia completa e quindi non è corretto usarli come motore automatico del prezzo.

### Compatibilità stato

- `index.html` mantiene le chiavi storiche `astaPinta.state.v2`, `astaPinta.github.v1`, `astaPinta.data.v1`: l’aggiornamento non azzera lo stato stabile esistente.
- `merge()` continua ad aggiungere le nuove impostazioni mancanti partendo da `config.json`, quindi uno stato v2 preesistente riceve automaticamente `profiloBudget`.
- `beta.html` usa invece `astaPinta.beta.*` e il branch `stato-beta`.
