# Guida tecnica sintetica — Asta AS Pinta v2.7

Per lo sviluppo successivo il documento canonico è **HANDOFF_CLAUDE_v2.7.md**. Questa guida riassume solo l'uso operativo.

## Durante l'asta

- **Cerca**: nome estratto -> scheda -> radio esito -> prezzo -> OK.
- **Prezzo mancante**: registrabile, ma sempre segnalato come dato da verificare.
- **Da foto**: un solo prompt, dati squadra e/o assegnazioni nello stesso blocco. Merge conservativo.
- **Obiettivi**: cockpit strategico; MUST/evita in testa; alert dati; priorità; CheckAI; mercato mirato.
- **Rosa**: cassa, ruoli, rischio buchi, moduli Mantra, campo XI, budget reparto.
- **Rivali**: potere d'acquisto e rilancio massimo; tocca una card per aprire la rosa per ruolo.
- **Condividi stato**: HTML autonomo per Ric.
- **CheckAI**: Markdown completo da caricare/incollare in un chatbot per secondo parere strategico.

## Concetti prezzo

- **Stima mercato**: prezzo atteso dalla taratura FVM.
- **Tetto strategico AS Pinta**: valore massimo del giocatore per qualità/ruolo/scarsità/strategia.
- **Limite operativo oggi**: quanto puoi davvero offrire ora, dopo riserve, slot e MUST.

## Qualità dati

Uno stato con squadra nota ma prezzo ignoto è preferibile a perdere l'assegnazione. L'app lo conserva e lo mette in alert finché il prezzo viene completato. L'import successivo con prezzo deve integrare il record, non crearne uno nuovo.

## Gruppo Esperti

In `players.json` alcuni profili principali hanno `ge`, `geScore`, `geSrc`. La copertura è deliberatamente parziale; è un enrichment di supporto e non sostituisce score/tetti AS Pinta.
