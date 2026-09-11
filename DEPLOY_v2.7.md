# Deploy v2.7 — checklist rapida

## 1. Backup prima di sostituire i file

Dall'app stabile attuale: **Impostazioni → Backup manuale → Scarica file di backup**. Non azzerare il browser.

## 2. File da caricare sul branch `main`

Sostituire/caricare:

- `index.html`
- `beta.html`
- `.nojekyll`
- `data/players.json`
- `data/config.json`
- `data/shortlist.json`

I documenti `.md` non sono necessari al funzionamento ma sono consigliati nel repo.

## 3. Attendere GitHub Pages

Dopo il commit attendere 1–2 minuti e fare refresh completo. `index.html` usa lo stato stabile; `beta.html` usa stato isolato.

## 4. Smoke test su `beta.html`

Fare, nell'ordine:

1. Cerca `Svilar`: i suggerimenti devono apparire subito mentre scrivi.
2. Apri Svilar: in alto devono esserci **Segna MUST / Segna da evitare** e l'Identikit deve mostrare la dritta Gruppo Esperti.
3. Registra un rivale **senza prezzo**: deve comparire una conferma esplicita e poi l'alert `⚠ prezzi`.
4. Vai in **Obiettivi**: il nome senza prezzo deve apparire in `Controllo puntuale richiesto`.
5. **Da foto**: incolla un blocco misto squadra + giocatori. Il merge deve integrare e non cancellare i campi vuoti.
6. **Rivali**: tocca direttamente la card di Fight Club (o altra squadra con nomi noti). La rosa deve aprirsi dentro la card, per ruolo.
7. **Rosa**: controlla il modulo guida e il campo verde; ogni giocatore va usato una sola volta nello XI.
8. **Obiettivi → CheckAI**: deve scaricare un `.md` e tentare anche la copia negli appunti.
9. **Condividi stato** dalla Rosa: deve generare HTML autonomo.
10. Test `↶ Annulla` dopo una registrazione.

## 5. Passaggio alla stabile

Se i test sopra sono ok, aprire `index.html` e verificare che lo stato stabile precedente sia ancora presente. Il branch GitHub della stabile resta `stato`; il beta resta `stato-beta`.
