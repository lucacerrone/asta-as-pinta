# Asta AS Pinta: audit UI/UX, piano patch e test di regressione (v2.7.1-beta)

## 1. Audit rapido

Eseguito su iPad orizzontale (1180×820), iPad verticale (820×1180) e iPhone (390×844), con i dati di `TEST_ASTA_4_UPDATE.txt` caricati.

| # | Problema osservato | Impatto in asta |
|---|---|---|
| A1 | Nella scheda il pulsante **OK** finisce sotto la piega: le 16 scelte di esito in 3 colonne occupano circa 450 px | Scroll obbligatorio a ogni estrazione |
| A2 | L'etichetta "fino a" si sovrappone al numero del verdetto | Numero chiave meno leggibile |
| A3 | **Stima / Tetto / Limite** stanno sotto il form di registrazione, con spiegazioni lunghe | I tre numeri decisivi non si vedono insieme al verdetto |
| A4 | La scarsità compare due volte (nel verdetto e in un box separato); l'infortunio è in un box alto | Rumore |
| A5 | La scelta selezionata si vede appena (solo bordo) | Rischio di confermare la squadra sbagliata |
| A6 | Barra superiore alta 126 px su iPhone (tre righe di pill) | Poco spazio utile |
| A7 | I box di spiegazione in Rosa, Rivali e Obiettivi sono sempre aperti | Pagine lunghe, contenuto operativo spinto in basso |
| A8 | La notifica copre il fondo dello schermo (OK e navigazione) | Feedback che nasconde i comandi |
| A9 | Card rivali alte, numero azionabile (rilancio max) in piccolo in fondo | Serve più di 3 secondi per leggere chi ha cassa |
| A10 | Su iPhone "Annulla" finisce a destra, fuori schermo nella barra scorrevole | Serve uno scroll orizzontale |

## 2. Piano di patch

| Priorità | Modifica | Beneficio | Rischio regressione | File e funzioni |
|---|---|---|---|---|
| **P0** | **Import: riga senza separatori** (`Dybala Big Tasty FC 52`) registra il giocatore senza squadra né prezzo. Presente anche nella v2.7 (vedi 3.3) | Dati corretti; scompare il falso "⚠ prezzi" | Basso: una condizione in un solo punto | `beta.html` / `index.html` → `parseImport` |
| P1 | OK sticky, griglia esiti densa, selezione piena (A1, A5) | Registrazione senza scroll | Nessuno sulla logica (solo CSS e classi) | CSS; `card()` (solo classi) |
| P1 | Fix etichetta "fino a" (A2) | Verdetto leggibile | Nullo | CSS |
| P1 | "Tre numeri" subito sotto il verdetto; infortunio compatto; scarsità non duplicata (A3, A4) | Decisione con una sola occhiata | Basso: riordino markup, stesse funzioni di calcolo | `card()` |
| P1 | Spiegazioni richiudibili (A7) | Pagine molto più corte | Basso: stesso testo dentro `<details>` | `helpBox()` + CSS |
| P1 | Barra superiore su una riga con ordine per importanza (A6) | Da 126 a 56 px su iPhone | Basso: classi aggiunte alle pill | `render()` (solo markup) + CSS |
| P1 | Notifica in alto (A8) | Non copre più OK e navigazione | Nullo | CSS |
| P1 | Rivali più densi, rilancio max in grande (A9) | Più squadre per schermata | Nullo | CSS |
| P2 | Pill "Annulla" fissa a sinistra o icona nella barra di ricerca (A10) | Annulla sempre a portata | Basso | `render()` |
| P2 | Pannello sinistro vuoto su iPad orizzontale con scheda aperta: mostrare alternative o ultimi passaggi | Sfrutta lo spazio | Medio (regola "i suggerimenti non vanno coperti") | `viewCerca()` |
| P2 | Obiettivi: accorciare la testata (CheckAI e hero più compatti) | Cockpit più leggibile | Basso | `viewObiettivi()` |
| P2 | Campo tattico: nomi più grandi su iPhone | Leggibilità | Basso | CSS `.pitch`, `formationField()` |
| P2 | Microcopy uniforme (es. "Mov fino a" / "Limite operativo" / "puoi arrivare a") | Coerenza | Basso | vari template |

## 3. Rilascio v2.7.1 (P0 + P1, su index.html e beta.html)

`index.html` e `beta.html` sono identici tranne `data-channel="beta"` e `APP_VERSION`. Memoria e branch restano separati:
- stabile: `astaPinta.state.v2` e branch `stato`;
- beta: `astaPinta.beta.state.v2` e branch `stato-beta`.

**P0: `parseImport`.** Una riga senza separatori che contiene squadra o numeri non viene più letta tutta come nome, ma passa al parser tollerante.
- `Dybala Big Tasty FC 52` → Big Tasty FC, 52;
- `Martinez L. S.S. Longobarda 105` → S.S. Longobarda, 105.

**P1: interfaccia** (solo CSS e template: `card`, `helpBox`, `render`).
- OK sempre visibile, griglia esiti densa, selezione piena;
- etichetta "fino a" non più sovrapposta;
- tre numeri (stima, tetto, limite) sotto il verdetto; infortunio compatto; scarsità non duplicata;
- spiegazioni richiudibili;
- barra superiore su una riga;
- notifiche in alto;
- Rivali più densi.

## 4. Test eseguito su index.html (v2.7 stabile originale contro v2.7.1), iPad 1180×820 e iPhone 390×844

Scenario:
- `TEST_ASTA_4_UPDATE`, UPDATE 1 e 2;
- Orsolini scartato; Zaccagni a Fight Club senza prezzo; Kean nostro a 40;
- Scamacca a NewRock seguito da Annulla;
- UPDATE 3 e 4; correzione `Zaccagni;Fight Club;9`;
- tutte le schede e una card rivale aperta.

| Controllo | v2.7 | v2.7.1 |
|---|---|---|
| Suggerimenti live, ritorno ricerca vuota, scartato ripescabile, alert prezzo, card rivale | PASS | PASS |
| Assegnati attesi dal file di test (Svilar 25, Calhanoglu 84, Mancini Space Invaders 31, **Dybala 52**, Pulisic 45, Malen 65, Hojlund 92, Martinez L. 105, Thuram 72, Orsolini Fun Cool FC 28) | FAIL (Dybala senza prezzo) | **PASS** |
| Alert prezzi scompare dopo le correzioni | FAIL | **PASS** |
| Crediti AS Pinta a fine scenario | 195 | 195 |
| Annulla ultima azione | PASS | PASS |
| OK visibile senza scroll | FAIL | **PASS** |
| Barra superiore iPhone | 126 px | **56 px** |
| Errori JavaScript | 0 | 0 |
| Differenze di stato tra le due versioni | · | solo `asg/Dybala/p` (atteso, fix P0) e le righe di `log` e `updates` |
| Canale | · | index: stato stabile · beta: stato separato |

Per rieseguire: `python3 docs/test_regressione_v2_7_1.py index_v27_orig.html index.html`, dalla cartella del repo con un server locale avviato dallo script e con `TEST_ASTA_4_UPDATE.txt` nel percorso indicato in testa allo script.

## 5. P2 rimasti (dopo l'asta)
- Pill "Annulla" sempre visibile su iPhone.
- Pannello sinistro vuoto su iPad orizzontale.
- Testata Obiettivi più compatta.
- Campo tattico più leggibile su iPhone.
- Microcopy uniforme.
