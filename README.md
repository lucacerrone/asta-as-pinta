# Asta AS Pinta — v2.7

Web-app statica per l'asta **FantaEnel 1X2**, modalità **Mantra**, 14 squadre, 500 crediti. È pensata per iPad/iPhone durante un'asta random totale: cerchi il giocatore appena estratto, leggi il consiglio operativo e registri l'esito.

## File

- `index.html` — versione stabile v2.7, usa `localStorage` e branch GitHub `stato`.
- `beta.html` — canale di prova isolato, usa memoria separata e branch `stato-beta`.
- `data/players.json` — listone e metadati giocatore. Juventus e Lazio sono presenti ma per AS Pinta sono “ultima spiaggia”.
- `data/config.json` — squadre, regole, strategia, preset budget, MUST/evita.
- `data/shortlist.json` — al momento vuoto (`[]`); può essere riempito senza cambiare il codice.
- `HANDOFF_CLAUDE_v2.7.md` — documento principale per continuare lo sviluppo.
- `DEPLOY_v2.7.md` — caricamento su GitHub e smoke test.
- `TEST_ASTA_4_UPDATE.txt` — 4 snapshot progressivi per stressare import/merge.

## Flusso d'asta consigliato

1. **Cerca** il cognome appena esce.
2. Leggi **Consiglio d'asta**, stima mercato, tetto strategico e limite operativo.
3. Inserisci il prezzo, seleziona con radio button **AS Pinta / Scartato / squadra rivale / ?** e premi **OK**.
4. Se registri un assegnato senza prezzo, l'app lo accetta ma lo marca come dato da verificare: compare un alert in alto e in **Obiettivi**.
5. Ogni tanto usa **Da foto** con il prompt unico: può contenere nello stesso incolla sia snapshot squadra sia assegnazioni.
6. Controlla **Obiettivi** per strategia live, MUST/evita, CheckAI e buchi del modulo; **Rosa** per moduli Mantra e campo tattico; **Rivali** per potere d'acquisto e rose nominali.

## Fonti dati principali

- Fantacalcio.it / Leghe Fantacalcio: quotazioni, FVM, ruoli Mantra e dati ufficiali di supporto.
- SOS Fanta: fasce e guide Mantra usate nella costruzione iniziale del dataset.
- Forum Gruppo Esperti, topic schede 2026/27: `https://forum.gruppoesperti.it/viewtopic.php?t=232729` — in v2.7 è stata integrata una **prima copertura curata di 19 profili principali**, non ancora l'intero listone.

## Importante

`index.html` e `beta.html` condividono la stessa logica ma **non lo stesso stato**. Testare prima su `beta.html`; quando soddisfatti, usare `index.html` senza azzerare la memoria stabile.
