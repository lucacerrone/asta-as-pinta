# Deploy v2.7.1: 5 minuti

1. **Backup:** dall'app attuale, *Impostazioni > Backup manuale > Scarica file di backup*. Non azzerare il browser.
2. **Carica su `main`:** in GitHub *Add file > Upload files*. **Obbligatori** `index.html` e `beta.html`, che sostituiscono i vecchi. Cartella `data/` invariata rispetto alla v2.7: ricaricarla non fa danni. `docs/` e `README.md` sono facoltativi.
3. **Commit sul branch `main`**, non su `stato` né su `stato-beta`. Attendi 1-2 minuti e ricarica completamente la pagina in Safari.
4. **Verifica versione:** in *Impostazioni*, `index.html` deve dire **2.7.1** e `beta.html` **2.7.1-beta**.
5. **Smoke test su `index.html`, 2 minuti:**
   - lo stato precedente c'è ancora (crediti e rosa invariati);
   - cerca un nome e aprilo: sotto il verdetto ci sono i tre numeri, "FINO A" non è sovrapposto;
   - tocca una squadra: diventa bordeaux piena, e OK è visibile senza scroll;
   - **non registrare test sulla stabile**: per le prove usa `beta.html`.
6. **Test del parser, se vuoi, su `beta.html`:** Da foto > incolla `Dybala Big Tasty FC 52` > Leggi. Deve risultare Big Tasty FC, 52.
