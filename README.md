# Asta AS Pinta — v2.1

Web app statica per l’asta **Mantra FantaEnel 1X2**: cerchi il giocatore appena uscito e ottieni subito verdetto, tetto, motivazione e alternative. È pensata soprattutto per Safari su iPad/iPhone e gira su GitHub Pages.

## File da pubblicare

| File | Cosa contiene |
|---|---|
| `index.html` | app stabile |
| `beta.html` | canale di prova, con memoria separata e branch `stato-beta` |
| `data/players.json` | listone: **507 giocatori**, inclusi Juventus e Lazio |
| `data/shortlist.json` | shortlist Piano A/B/C già presente nel repo |
| `data/config.json` | lega, prezzi, MUST/evita, squadre da evitare e preset budget |
| `README.md` / `GUIDA_asta-as-pinta.md` | istruzioni e handoff tecnico |

Lo stato reale dell’asta resta salvato in `localStorage` e, se colleghi GitHub, in `data/state.json` sul branch **`stato`**. `beta.html` usa chiavi `localStorage` diverse e forza il branch **`stato-beta`**, quindi può essere provato senza toccare l’app vera.

## Novità operative v2.1

- **Juventus e Lazio sono nel listone** e si possono assegnare normalmente. Per AS Pinta sono però marcati di default come **“Evita — ultima spiaggia”**, con tetto base a **1 credito**; un MUST manuale può sovrascrivere questa regola.
- Ogni scheda ha un **“Perché”**. Il dataset usa soltanto informazioni già ricavate da **SOS Fanta** e **Fantacalcio.it**; i dati base erano aggiornati al 10/09, con integrazione Juve/Lazio all’11/09/2026.
- Layout più denso su iPhone/iPad. In **iPad landscape**, durante una ricerca, risultati e scheda giocatore sono affiancati.
- **Alternative immediate (F10)**: 3 migliori giocatori liberi dello stesso ruolo top.
- **Annulla ultima azione (F1)**: pulsante sempre visibile in alto; `F1` da tastiera fa la stessa cosa.
- **Modalità asta (F4)**: pulsanti/verdetto ingranditi, tab nascoste, nuova ricerca automatica dopo un’assegnazione; `F4` da tastiera la attiva/disattiva.
- **Scarsità per ruolo (F3)** con lieve correzione del tetto; **rischio buco (I1)** e **chiudi ora a 1–3 crediti (I4)** in Rosa.
- **Cruscotto (V1)** e **potere d’acquisto rivali (V2)**. Gli indicatori che dipendono dagli screenshot sono esplicitamente trattati come fotografie, non come cronologia perfetta.
- **Budget per reparto (F6)** con tre preset configurabili. Le percentuali incluse sono preset operativi provvisori perché il vecchio Excel con i valori originari non era tra i file ricevuti.
- **Import screenshot “a salti”**: una riga nuova corregge/completa lo stato precedente; ciò che non appare nello screenshot non viene cancellato.

## Pubblicazione rapida

Nel repo `asta-as-pinta`, carica/sostituisci `index.html`, aggiungi `beta.html`, sostituisci `data/players.json` e `data/config.json`, quindi aggiorna README/guida. GitHub Pages continua a pubblicare dal branch `main`/root.

Per lo stato live crea un token Fine-grained con accesso solo al repo e **Contents: Read and write**. Nell’app stabile collega GitHub da **Impostazioni**: verrà usato il branch `stato`. In `beta.html` il branch è bloccato a `stato-beta`.

## Uso durante l’asta

1. In **Cerca**, digita 2–4 lettere del cognome e apri il giocatore.
2. Leggi verdetto e massimo. La scarsità, quando rilevante, è già evidenziata.
3. A fine rilancio usa **Preso da noi** oppure **Preso da altri**. Se inserisci squadra+prezzo, il rivale viene aggiornato subito.
4. Ogni tanto fai uno screenshot e usa **Da foto**. Lo screenshot più recente vince per le righe che contiene; non serve seguire ogni singola estrazione.
5. Controlla **Rosa** per rischi di buco, candidati da 1–3 crediti, budget per reparto e cruscotto; **Rivali** è già ordinato per crediti/slot.
6. Se sbagli un’azione, usa **↶ Annulla** in alto.

## Da evitare / MUST

`data/config.json` supporta sia nomi singoli sia squadre:

```json
"must": [{"n":"Dybala","max":80,"why":"motivo"}],
"evita": ["Varela G."],
"evitaSquadre": ["Juventus", "Lazio"],
"ultimaSpiaggia": {"prezzo":1}
```

I nomi vanno scritti come nel listone. Un giocatore segnato manualmente come MUST ha precedenza sul “da evitare per squadra”.

## Backup e problemi

- verde = stato salvato su GitHub; giallo = salvataggio in corso; blu = solo dispositivo; rosso = errore GitHub;
- **Impostazioni > Scarica file di backup** crea un backup manuale;
- il token resta solo sul dispositivo;
- non usare navigazione privata;
- se cambi dispositivo, collega lo stesso repo/token e usa **Ricarica da GitHub** se serve.

Dopo l’asta revoca il token. La cronologia Git del branch `stato` resta disponibile come ulteriore traccia dei salvataggi.
