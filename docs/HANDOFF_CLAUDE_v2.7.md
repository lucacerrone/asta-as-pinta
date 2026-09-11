# HANDOFF CLAUDE — Asta AS Pinta v2.7

**Data handoff:** 11/09/2026, immediatamente pre-asta.  
**Obiettivo del prossimo passaggio:** fare un audit esperto **UI/UX** senza rompere la logica già funzionante, rendere l'interfaccia ancora più infografica/leggibile e proseguire solo sulle feature ad alto valore operativo.

---

## 0. Regola fondamentale per continuare

Non riscrivere l'app da zero. La v2.7 è già un'app operativa, testata progressivamente dall'utente. Procedere per patch piccole su `beta.html`, usare `index.html` solo dopo smoke test.

La priorità assoluta è il **flusso durante l'asta**: velocità, assenza di ambiguità, prevenzione degli errori di stato. Qualsiasi miglioramento estetico deve preservare densità informativa e numero minimo di tap.

---

# 1. Contesto lega

- Lega **FantaEnel 1X2**.
- Piattaforma Leghe Fantacalcio, modalità **Mantra**.
- 14 squadre, 500 crediti ciascuna.
- Asta **random totale**: il nome estratto non è chiamato da noi.
- Rosa: 2–4 portieri; 23–26 movimento; 25–30 totali.
- AS Pinta = squadra dell'utente + Ric.
- Juventus e Lazio sono nel listone ma per scelta AS Pinta vengono trattate come **ultima spiaggia, max 1 credito**.
- La lega parte dalla 5ª giornata di Serie A.
- Sostituzioni BASIC Mantra: l'app usa gli 11 moduli ufficiali per ragionare sulla copertura senza malus.

---

# 2. Architettura tecnica attuale

App volutamente semplice:

```text
index.html / beta.html
  ├── fetch data/players.json
  ├── fetch data/config.json
  ├── fetch data/shortlist.json
  ├── localStorage stato immediato
  └── GitHub REST -> data/state.json su branch dedicato
```

Nessun framework, nessun backend, nessuna libreria esterna runtime. HTML/CSS/JS vanilla in un solo file per massima affidabilità in asta.

### Canali

- `index.html`: nessun `data-channel="beta"`; localStorage stabile + branch GitHub `stato`.
- `beta.html`: `<html data-channel="beta">`; localStorage separato + branch `stato-beta`.

Non cambiare questa separazione.

---

# 3. Dati

## players.json

Campi storici principali:

- `n` nome listone
- `t` squadra Serie A
- `r` ruoli Mantra separati da `;`
- `tr` ruolo guida
- `ft` fascia top
- `fr` fasce per ruolo
- `s` titolarità
- `rg` ordine rigoristi
- `pz` piazzati
- `i` infortunio
- `sc` score 0–100
- `c` consiglio base
- `f` fattore tetto
- `fv` FVM
- `fe` FVM stimato sì/no
- `no` lettura AS Pinta

### Novità v2.7 Gruppo Esperti

Per **19 profili principali** sono stati aggiunti:

- `geScore` — punteggio “Consiglio Esperti” sintetico /10.
- `ge` — dritta breve e parafrasata, pensata per essere letta durante l'asta.
- `geSrc` — fonte/data.

Fonte: `https://forum.gruppoesperti.it/viewtopic.php?t=232729` (topic riassuntivo schede squadra 2026/27, consultato 11/09/2026).

La copertura NON è completa: non assumere che l'assenza di `ge` significhi giudizio negativo. È semplicemente un backlog di enrichment.

## config.json

Contiene:

- squadre e nome nostro;
- regole rosa;
- budget / tetto / stile / riserva / target;
- moltiplicatori prezzo;
- minimi prudenziali per ruolo;
- MUST / evita;
- Juventus/Lazio come `evitaSquadre`;
- prezzo/testo ultima spiaggia;
- profili `budgetReparti`.

Nota: i preset budget reparto (`Equilibrato`, `Stella`, `Bonus centrocampo`) sono **operativi/provvisori**, non derivano dal vecchio Excel originale.

## shortlist.json

Attualmente `[]`. Il codice supporta Piano A/B/C, ma in questa release non c'è una shortlist popolata.

---

# 4. Stato runtime

Struttura essenziale:

```json
{
  "set": {...},
  "mine": [{"n":"...","p":25}],
  "asg": {"Nome":{"t":"Fight Club","p":40,"s":1}},
  "riv": {"Fight Club":{"c":...,"g":...,"p":...}},
  "must": [{"n":"...","max":0}],
  "black": ["..."],
  "passed": [{"n":"...","ts":...}],
  "updates": [...],
  "log": [...]
}
```

### `asg.s`

`s:1` indica che il prezzo è già stato sottratto manualmente/operativamente al rivale. L'import da foto è volutamente conservativo per non sottrarre due volte.

### Prezzo mancante — NOVITÀ v2.7

È consentito registrare un assegnato senza prezzo perché durante l'asta può capitare di conoscere nome/squadra ma non il prezzo. Non deve però passare inosservato:

- al salvataggio manuale compare `confirm()`;
- topbar mostra `⚠ prezzi N`;
- Obiettivi mostra `Controllo puntuale richiesto` con elenco;
- import da foto segnala quanti prezzi restano da verificare;
- CheckAI esporta il problema nella sezione qualità dati.

Non trasformare in errore bloccante: la priorità è non perdere l'assegnazione.

---

# 5. Flusso Cerca / scheda giocatore

## Ricerca

- Gli ultimi passaggi sono mostrati solo quando il campo ricerca è vuoto.
- Appena l'utente digita, tutta l'area viene dedicata ai suggerimenti: questo comportamento è prioritario e non va regredito.

## Scheda

Ordine concettuale v2.7:

1. verdetto grande (`Prendi`, `MUST`, `Lascia`, ecc.);
2. consiglio d'asta contestuale in linguaggio da fantallenatore;
3. pulsanti in testa **Segna MUST / Segna da evitare**;
4. registrazione esito con radio button: `?`, `AS Pinta`, `Scartato`, tutte le squadre;
5. prezzo;
6. un solo `OK` -> registra e torna subito alla ricerca;
7. eventuali warning (infortunio/scarsità);
8. stima mercato / tetto strategico / limite operativo;
9. Identikit fantacalcistico;
10. alternative ancora libere.

### Identikit v2.7

È stato reso più leggibile:

- profilo rapido ruoli/fascia/titolarità;
- valutazione AS Pinta;
- **Dritta Gruppo Esperti** se disponibile;
- **Lettura AS Pinta** separata;
- dati tecnici completi chiusi in `<details>`.

MUST/Evita non sono più in fondo.

---

# 6. Import da foto

C'è **un solo prompt** in testa. La risposta può contenere contemporaneamente:

```text
Squadra;crediti;giocatori;portieri
Giocatore;Squadra;Prezzo
```

Regola fondamentale: **merge conservativo**.

- nuovo dato -> aggiunge;
- dato esplicitamente diverso -> corregge;
- campo vuoto/non letto -> conserva il valore già noto;
- riga assente -> non cancella nulla.

L'import non deve mai interpretare l'assenza da uno screenshot come cancellazione.

Usare `TEST_ASTA_4_UPDATE.txt` per regressione.

---

# 7. Rosa / Mantra

La schermata Rosa include:

- crediti disponibili;
- massimi operativi movimento/portiere tradotti in linguaggio utente;
- mercato della stanza (inflazione osservata, solo informativa);
- potere d'acquisto in `crediti per posto minimo ancora da coprire`;
- copertura prudenziale ruoli;
- rischio buco;
- analisi degli **11 moduli Mantra**;
- campo verde del miglior modulo, con ogni calciatore usato una sola volta nello XI;
- top 4 moduli + tutti gli 11 in details;
- budget reparto;
- acquisti e correzione prezzo;
- condivisione HTML dello stato.

Il motore dei moduli usa compatibilità di ruolo senza fuori ruolo e valuta quanti slot degli 11 sono già coperti. È una bussola di costruzione rosa, non un ottimizzatore perfetto di formazione settimanale.

---

# 8. Rivali v2.7

Ogni card mostra graficamente:

- crediti residui;
- posti minimi ancora da riempire;
- nomi noti / giocatori dichiarati dallo snapshot;
- potere d'acquisto;
- rilancio massimo teorico.

### Nuova UX

La rosa rivale NON è più una sezione separata sotto tutte le card. **Si apre toccando direttamente la card della squadra** e si espande nella card stessa, con giocatori divisi per ruolo Mantra.

I pluriruolo compaiono nei ruoli che possono coprire, ma il conteggio “nomi noti” resta distinto.

Se lo snapshot dice 12 giocatori ma conosciamo solo 7 nomi, l'interfaccia deve continuare a mostrare 7/12 e non inventare i 5 mancanti.

---

# 9. Obiettivi = Piano d'asta

Questa sezione non è più una shortlist passiva. Deve essere il **cockpit strategico**.

Ordine attuale:

1. **CheckAI**;
2. MUST / Evita ancora aperti, visibili subito in testa;
3. alert qualità dati (es. prezzi mancanti);
4. “Adesso” — consiglio principale;
5. mercato, potere d'acquisto, modulo guida, MUST liberi;
6. priorità operative;
7. campo del modulo guida;
8. giocatori mirati sui buchi;
9. gestione completa MUST;
10. evita;
11. scanner ruolo;
12. passati ancora liberi;
13. shortlist A/B/C (oggi vuota).

Questa gerarchia è intenzionale: prima strategia, poi scouting.

---

# 10. CheckAI — IMPLEMENTATO in v2.7

Pulsante `CheckAI · esporta stato completo` in Obiettivi.

Genera un file Markdown `AS-Pinta-CheckAI-....md` e tenta anche la copia negli appunti. Contiene:

- prompt già pronto per un chatbot esperto Mantra;
- situazione sintetica;
- strategia impostata;
- priorità app;
- rosa AS Pinta con prezzi;
- top moduli e buchi;
- rischio ruoli;
- budget reparto;
- MUST / evita;
- per ogni rivale: snapshot e rosa nominale nota;
- alert prezzi mancanti;
- ultimi update.

Scopo: caricarlo/incollarlo in ChatGPT/Claude e chiedere un **secondo parere sulla strategia**, senza dover ricostruire a mano lo stato.

---

# 11. Condividi stato (F9 reinterpretata)

Dalla Rosa viene generato un HTML autonomo condivisibile con Ric. Include:

- intro discorsiva situazione;
- ultimi due update;
- KPI;
- rosa e ruoli;
- moduli;
- MUST / low cost / passati liberi;
- rivali.

È una fotografia “read-only” al momento della condivisione, non una vista live.

---

# 12. UI attuale

Design già evoluto rispetto alla v2 iniziale:

- palette Roma-like (rosso/giallo) invece del viola originario;
- card morbide e compatte;
- SVG inline self-contained, ispirazione Lucide;
- bottom nav;
- KPI, barre, ring di progresso, campo verde, badge squadre;
- responsive iPhone/iPad; split ricerca/dettaglio in landscape quando possibile.

## Richiesta esplicita dell'utente per il prossimo passaggio

Fare una **ripassata esperta UI/UX** per renderla ancora più:

- infografica;
- moderna/premium;
- immediatamente leggibile sotto pressione;
- coerente tra sezioni;
- visuale, ma senza diventare dispersiva.

### Criteri dell'audit UI/UX

Valutare almeno:

1. gerarchia visiva e above-the-fold su iPad;
2. tap target e numero di tap per il flusso estrazione -> registrazione;
3. chiarezza dei termini per un fantallenatore avanzato, non per un programmatore;
4. densità: evitare box inutilmente alti;
5. colore solo quando ha significato reale; evitare finti semafori;
6. accessibilità/contrasto;
7. consistenza delle icone;
8. feedback immediato dopo azioni;
9. differenza chiara fra valore di mercato, strategia e limite operativo;
10. leggibilità del campo Mantra e dei moduli;
11. alert dati incompleti ben visibili ma non paralizzanti;
12. Rivali: capire in <3 secondi chi ha più cassa e quali ruoli/giocatori possiede.

Non sostituire SVG con CDN o dipendenze online: durante l'asta l'app deve restare autonoma.

---

# 13. Backlog residuo — priorità raccomandata

## P0 — da fare solo se emerge un bug nei test reali

- regressioni import merge;
- conteggi crediti/rosa incoerenti;
- assegnazioni duplicate;
- modulo che usa lo stesso calciatore due volte;
- radio esito che non resetta/torna alla ricerca;
- GitHub sync che tocca branch sbagliato.

Nessuna feature estetica deve precedere un P0.

## P1 — UI/UX audit richiesto dall'utente

**Da fare con Claude ora.** Rifinire senza riscrivere:

- sistema di griglia e spaziature;
- KPI più infografici;
- visual design delle priorità;
- rose rivali più scansionabili;
- campo tattico più leggibile;
- coerenza card / headings / microcopy;
- eventuali micro-animazioni solo se non compromettono velocità.

## P1 — Enrichment Gruppo Esperti completo

Oggi sono coperti 19 profili principali. Estendere `ge/geScore` all'intero listone o almeno a tutti i giocatori appetibili (`sc >= 48`) usando **solo il topic 2026/27** e parafrasi corte.

Regole:

- non copiare lunghi passaggi;
- massimo 1–2 frasi operative per giocatore;
- se il forum non dà un giudizio utile, lasciare vuoto;
- non confondere “Consiglio Esperti /10” con lo score AS Pinta /100.

## P1 — Audit completo ruoli/listone Fantacalcio.it

L'utente vuole Fantacalcio.it (ex Fantagazzetta) come riferimento ufficiale per rosa e ruoli. È stato fatto solo spot-check, non confronto automatico esaustivo dei 507 giocatori.

Da fare con calma:

- nome;
- squadra;
- ruoli Mantra;
- FVM;
- eventuali trasferimenti post dataset.

Generare report differenze prima di modificare `players.json`.

## P2 — Rose rivali più strategiche

Attuale: mostra nomi registrati per ruolo. Evoluzioni possibili:

- conteggio “slot tattici” delle rose rivali;
- loro moduli migliori stimati;
- evidenziare quale rivale è probabilmente in caccia di Pc/E/M ecc.

NON far entrare questa inferenza nei prezzi senza un indicatore di affidabilità, perché la rosa nominale dei rivali può essere parziale.

## P2 — Tattica Mantra avanzata

Attuale campo = miglior copertura statica della nostra rosa.

Possibili upgrade:

- top 2 XI alternativi;
- punteggio qualità XI, non solo numero slot coperti;
- “se compri X, il modulo sale da 8/11 a 10/11”;
- resilienza BASIC: quante sostituzioni possono essere assorbite senza malus;
- panchina consigliata post-asta.

Questa è utile, ma non va implementata all'ultimo minuto senza test.

## P2 — CheckAI v2

La prima versione è già presente. Possibili upgrade:

- scelta “breve / completo”;
- esportare anche JSON macchina;
- includere alternative migliori per ogni buco;
- indicatore di affidabilità dei dati rivali;
- pulsante Share Sheet iOS oltre a download+clipboard.

## P3 — Backlog storico NON urgente

- F2 inflazione che modifica automaticamente i prezzi: **non consigliato** finché gli assegnati registrati sono incompleti; oggi inflazione è solo un termometro.
- F7 costruttore formazione/panchina settimanale completo: post-asta.
- V3 ultimi assegnati/affari: rischia di suggerire una cronologia che gli screenshot non garantiscono.
- V4 mappa ruoli/fasce separata: parzialmente superata da Rosa + Obiettivi.
- V5 grafico pagato vs stimato: cosmetico/analitico.
- I2 forza rose rivali: dati nominali troppo incompleti.
- I3 news automatiche live: richiede servizio esterno o aggiornamento dati; non inserirlo in un HTML statico senza architettura dedicata.

---

# 14. Test di regressione obbligatori dopo ogni patch

Usare `TEST_ASTA_4_UPDATE.txt` e fare almeno:

1. ricerca live non coperta dagli ultimi passaggi;
2. giocatore -> radio esito -> OK -> ritorno ricerca vuota;
3. Scartato resta libero e ripescabile;
4. assegnato senza prezzo -> alert persistente;
5. import successivo con prezzo -> alert scompare;
6. campo vuoto import NON cancella dato esistente;
7. squadra assente da snapshot NON viene azzerata;
8. correzione esplicita prezzo/squadra sostituisce dato vecchio;
9. Rivali card -> espansione rosa corretta;
10. pluriruolo rappresentato nei ruoli possibili senza gonfiare numero nomi;
11. CheckAI contiene prezzi mancanti e rosa/rivali;
12. campo modulo non duplica giocatore;
13. beta salva su `stato-beta`; stabile su `stato`;
14. undo funziona sull'ultima azione mutante.

---

# 15. Funzioni chiave nel JS

Cerca questi nomi, non lavorare “a vista” sul file:

### Stato/persistenza
`defaults`, `merge`, `loadLocal`, `persist`, `logEvent`, `recordUpdate`, `removeKnownAssignment`, `saveUndo`, `undoLast`

### Prezzi/strategia
`market`, `baseMax`, `maxFor`, `me`, `rivMax`, `topRival`, `verdict`, `expertAdvice`, `auctionStats`, `marketMood`, `strategyPriorities`, `strategyCandidates`

### Ruoli/Mantra
`rolesOf`, `formationAnalysis`, `formationCard`, `formationField`, `holeRisks`, `scarcityForPlayer`, `roleCountMine`

### Rivali
`rosterForTeam`, `rivalRosterBody`, `viewRivali`

### Import
`PROMPT_FOTO`, `parseImport`, `applyImport`, `viewImporta`

### Export
`stateSnapshotHTML`, `shareState`, `checkAIText`, `downloadText`

### UI
`render`, `viewCerca`, `card`, `viewRosa`, `viewRivali`, `viewObiettivi`, `viewImpostazioni`

---

# 16. Cose da NON fare

- non cancellare lo stato perché uno screenshot non contiene una riga;
- non far decrementare due volte i crediti rivali;
- non trattare una rosa rivale parziale come completa;
- non usare colori apparentemente semaforici senza significato;
- non nascondere i suggerimenti di ricerca con widget secondari;
- non chiedere conferme aggiuntive per ogni azione normale: solo quando c'è rischio reale, come prezzo mancante;
- non rendere il campo Mantra una simulazione “scientifica” se l'algoritmo è solo euristico;
- non far diventare le note Gruppo Esperti una copia integrale del forum;
- non aggiungere dipendenze esterne necessarie al runtime.

---

# 17. Stato dei test a questo handoff

- `node --check` sul JS v2.7: **PASS**.
- runtime headless VM con dataset reale: **PASS** per:
  - motore moduli;
  - campo tattico;
  - Obiettivi;
  - rose rivali inline;
  - import misto squadre+giocatori;
  - CheckAI;
  - dritta GE su giocatore campione.
- Non è stato eseguito in questo ambiente un vero Playwright end-to-end su Safari/iPad. L'utente deve fare smoke test browser reale.

---

# 18. Prima richiesta consigliata a Claude

> Leggi integralmente HANDOFF_CLAUDE_v2.7.md, index.html, beta.html, config.json e players.json. Non riscrivere l'app. Fai prima un audit UI/UX esperto dell'interfaccia attuale pensando a un fantallenatore Mantra avanzato che usa iPad sotto pressione durante un'asta random. Proponi un piano di patch prioritizzato P0/P1/P2, indicando per ogni modifica beneficio, rischio di regressione e file/funzioni coinvolte. Poi implementa esclusivamente il blocco P1 UI/UX su beta.html, mantenendo invariata la logica di stato/import/prezzi, e prepara un test di regressione.

