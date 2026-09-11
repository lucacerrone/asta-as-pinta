# Deploy v2.1 — checklist rapida

Sostituisci/carica nel branch `main` del repo:

1. `index.html` → sostituisce l'app stabile.
2. `beta.html` → nuovo file di test isolato.
3. `data/players.json` → sostituisce il listone.
4. `data/config.json` → sostituisce la configurazione.
5. `README.md` e `GUIDA_asta-as-pinta.md` → documentazione aggiornata.

**Non eliminare `data/shortlist.json`: non era tra i file caricati in questa sessione e non è stato modificato.**

Dopo il commit:

- apri prima `.../asta-as-pinta/beta.html`;
- collega GitHub: in beta il branch è forzato a `stato-beta`;
- prova ricerca di `Kolo Muani`: deve apparire `Evita — ultima spiaggia`, max 1;
- prova un giocatore normale e verifica `Perché` + 3 alternative;
- prova `↶ Annulla`, `Da foto`, `Rosa`, `Rivali`;
- solo dopo passa a `index.html` per l'asta reale.

Test eseguiti sul batch: JSON validi; 507 giocatori senza duplicati; 30 Juventus + 30 Lazio; nessuna nota `Perché` vuota; sintassi JavaScript valida; smoke test UI headless su ricerca, ultima spiaggia, alternative, split iPad, layout mobile, modalità asta, undo, cruscotto, potere d'acquisto, correzione da screenshot e isolamento beta.
