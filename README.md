# Asta AS Pinta

App per l'asta Mantra FantaEnel 1X2: cerchi il giocatore uscito e ti dice se prenderlo e fino a quanto. Funziona da Safari su iPad e iPhone, ospitata gratis su GitHub Pages.

## File

| File | Cosa contiene | Chi lo modifica |
|---|---|---|
| `index.html` | L'app (unico punto d'ingresso) | nessuno |
| `data/players.json` | Listone: 451 giocatori, ruoli, fasce, FVM, note (Juve e Lazio esclusi) | nessuno |
| `data/shortlist.json` | Obiettivi Piano A/B/C per reparto | volendo |
| `data/config.json` | Squadre, regole rosa, prezzi, impostazioni iniziali, MUST, da evitare | voi (anche Ric) |
| `data/state.json` sul branch **stato** | Stato dell'asta: nostri acquisti, assegnati, crediti rivali, storico | l'app, da sola |

Lo stato viene salvato in due posti: subito sul dispositivo (resiste alla chiusura di Safari) e, dopo pochi secondi, su GitHub (resiste anche al cambio di dispositivo). Sta su un branch separato perché ogni salvataggio sul branch principale farebbe ripubblicare il sito.

## Messa online (circa 10 minuti, meglio dal PC)

1. **Crea il repository.** Su github.com: *New repository*, nome `asta-as-pinta`, visibilità **Public** (GitHub Pages gratuito richiede un repo pubblico; dentro ci sono solo dati di fantacalcio, il token non finisce mai nel repo).
2. **Carica i file.** Nel repo: *Add file > Upload files*, trascina `index.html`, `README.md`, `.nojekyll` e la cartella `data`, poi *Commit changes*.
3. **Attiva Pages.** *Settings > Pages > Build and deployment*: Source **Deploy from a branch**, Branch **main** e cartella **/ (root)**, *Save*. Dopo 1-2 minuti il sito è su `https://TUO-UTENTE.github.io/asta-as-pinta/`.
4. **Crea il token.** Foto profilo > *Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token*:
   - nome `asta`, scadenza 7 giorni;
   - *Repository access*: **Only select repositories** > `asta-as-pinta`;
   - *Permissions > Repository permissions*: **Contents: Read and write**;
   - genera e copia il token (`github_pat_...`).
5. **Collega l'iPad.** Apri il link in Safari > scheda **Impostazioni** > scrivi utente GitHub e token > **Collega e sincronizza**. Il branch `stato` e il file `data/state.json` vengono creati da soli. Il pallino in alto diventa verde.

## Stasera

- **Una sola "porta" d'ingresso.** O la scheda di Safari, o l'icona in Home (*Condividi > Aggiungi alla schermata Home*): l'icona ha una memoria separata da Safari, quindi il token va inserito lì dove userai l'app. Niente navigazione privata.
- **Pallino in alto:**
  - verde = salvato su GitHub;
  - giallo = sto salvando;
  - blu = salvato solo sul dispositivo;
  - rosso = errore (toccalo per il dettaglio).
- **Cambio dispositivo:** collega GitHub anche sull'altro dispositivo. All'avvio l'app carica da sola la versione più recente; in alternativa c'è *Ricarica da GitHub*.
- **Emergenza:** *Impostazioni > Scarica file di backup*.

## MUST e da evitare modificati da GitHub (anche da Ric)

1. Apri `data/config.json` nel repo, icona matita.
2. Compila, per esempio:
   ```json
   "must": [ {"n": "Dybala", "max": 80, "why": "idolo di Ric"} ],
   "evita": [ "Varela G." ]
   ```
3. *Commit changes*, aspetta un minuto, poi nell'app: **Obiettivi > Importa MUST e da evitare da config.json**.

I nomi vanno scritti come nel listone ("Martinez L.", "Paz N.", "Calò"): per controllarli cercali nell'app. Se un nome non è nel listone, l'app lo segnala.

## Dopo l'asta

- Sul branch `stato`, la *History* di `data/state.json` è lo storico completo dell'asta: ogni salvataggio è un commit.
- Revoca il token: *Settings > Developer settings > Fine-grained tokens > Delete*.

## Problemi comuni

| Messaggio | Cosa fare |
|---|---|
| Token non valido o scaduto | Ricopia il token per intero o creane uno nuovo |
| Il token non ha il permesso di scrittura | Nel token imposta *Contents: Read and write* |
| Repository non trovato | Controlla utente e nome del repo, e che il token abbia accesso a quel repo |
| L'app non riesce a partire | Aprila dal link di GitHub Pages, non come file; controlla che la cartella `data` sia stata caricata |
| Offline | L'app usa i dati già scaricati, salva sul dispositivo e riprova da sola a salvare su GitHub |
