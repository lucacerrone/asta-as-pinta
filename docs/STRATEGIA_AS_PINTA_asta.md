# AS Pinta: strategia d'asta, checklist e configurazione

Lega FantaEnel 1X2 Mantra: 14 squadre, 500 crediti, asta random, rosa 2-4 Por + 23-26 Mov. I prezzi di questo documento sono calcolati con le formule della v2.7.1 (tetto 25%, stile Normale), **prima** dell'aggiustamento di scarsità che l'app applica in asta.

---

## 1. Checklist da compilare con Ric (5 minuti)

Metti una X. La **proposta** è già segnata ✅; se la cambiate, la sezione 5 dice cosa ritoccare.

| # | Decisione | Opzioni |
|---|---|---|
| 1 | Modulo guida | ✅ **4-2-3-1** · ☐ 4-3-1-2 · ☐ 4-3-3 · ☐ 3-4-2-1 |
| 2 | Punta stella (Malen ~223, Lautaro ~195) | ✅ **No** · ☐ Sì |
| 3 | Motore dei bonus | ✅ **Trequarti e centrali con rigori** · ☐ Calhanoglu (mercato ~136) |
| 4 | Portieri | ✅ **Titolare affidabile + 2° economico** · ☐ Svilar + low cost · ☐ due low cost |
| 5 | Tetto per singolo giocatore | ✅ **25% (125 cr)** · ☐ 30% · ☐ 45% (solo con stella) |
| 6 | Stile d'asta | ✅ **Normale** · ☐ Prudente · ☐ Aggressivo |
| 7 | Riserva per il finale | ✅ **30** · ☐ 20 · ☐ 40 |
| 8 | Giocatori in rosa | ✅ **27** · ☐ 25 · ☐ 30 |
| 9 | MUST extra-fanta, massimo 3 | 1. ______ max __ · 2. ______ max __ · 3. ______ max __ |
| 10 | Da evitare oltre Juve e Lazio | ✅ proposti: **Douvikas, Esposito F.P., Castro S., Varela G.** · aggiunte: ______ |
| 11 | Sforare il tetto di un OBIETTIVO | ✅ **massimo +10%** · ☐ mai |
| 12 | Crediti riservati ai MUST | ✅ **massimo 25% del budget (125 cr) in totale** |

---

## 2. Perché 4-2-3-1

**Il modulo**
- **Il listone Mantra 2026/27** ha pochissimi esterni **E** di livello (Dimarco, Wesley, Molina, Saelemaekers) e pochi mediani **M** con bonus. Abbondano invece Dc, C, W, T e punte.
- **Nel motore dell'app il 4-2-3-1** usa gli slot Ds · Dc · Dc · Dd · M · M/C · W/T · T · W/A · A/Pc: **nessun E**, un solo M puro, tre posti per trequartisti e ali, dove stanno i bonus.
- **Stessa base per le alternative:** 4-3-1-2 e 4-3-3 condividono difesa a 4 e mediano. Una rosa costruita per il 4-2-3-1 copre quasi gratis anche questi due moduli, e con le sostituzioni BASIC riduce i malus.
- **Il 3-4-2-1 stile Roma** richiede 2 E e 3 Dc: solo se a fine asta E e Dc sono arrivati a buon prezzo.

**Perché niente stella**
- Con 25-27 giocatori da comprare e 13 rivali, un giocatore al 40-45% del budget obbliga a riempire più di metà rosa a 1-3 crediti.
- Negli scontri diretti 1X2 conta la costanza di 11 titolari.
- Una Pc top da 90-125 crediti (Kean, Ramos G., Hojlund) più due trequartisti con rigori rende di più.

---

## 3. Piano per slot del 4-2-3-1

Nomi, piani, mercato e tetto nel file `shortlist.json`, che compare in **Obiettivi**. **A** = obiettivo, **B** = alternativa, **Value** = rapporto qualità/prezzo, **Panchina** = 1-15 crediti.

| Slot | Obiettivo A (mercato → tetto) | Alternative | Panchina |
|---|---|---|---|
| Por | Carnesecchi 33→36 · Maignan 30→33 | Butez 29→32 · Svilar 48→53 solo se scende | Skorupski 21 · Okoye 18 · Milinkovic-Savic V. 8 |
| Dc ×2 | Pavlovic 27→30 · Rrahmani 29→32 · Mancini 29→32 | Akanji, Chalobah T. (Dc/Dd), Gila · value Ostigard 22→24 (2° rig.), Vasquez 21→23 (Dc/Ds) | Theate 14 · Mina 13 · Comuzzo 8 |
| Dd | Di Lorenzo 24→26 | Vojvoda 12→13 · Jimenez A. 13→14 (Dd/Ds/E) · Belghali 12→13 | Bellanova 8 · Van Der Brempt 2 |
| Ds | Miranda J. 16→18 (piazzati) | Kamara H. 8→9 · Valeri 14 (3° rig.) · Spinazzola 16→18 | Mangas 10 · Gallo 2 |
| M | **Calò 21→23 (1° rig. + piazzati)** · Ederson D.S. 35→39 | Modric 29→32 · Konè M. 25→28 | Busio 8 (1° rig.) · Lobotka 18 · Frendrup 16 |
| M/C | **Da Cunha 49→54 (1° rig.)** · Atta 41→45 | Ekkelenkamp 33→36 · Barella 47→52 | Fazzini 18 · Thorstvedt 21 |
| T | **Vlasic 37→41 (1° rig.)** · De Bruyne 59→65 (1° rig.) | Pulisic 81→89 (top se sotto tetto) · Mora 57→63 | Adzic 10 · Maldini 16 |
| W/T | Goncalves P. 27→30 · Diao 41→45 | Politano 23→25 · Orsolini 76→61 (occasione: infortunato) | Schmid 15 (2° rig.) · Ghedjemis 18 |
| W/A | **Berardi 62→68 (1° rig.)** · Dybala 63→69 | Laurientè 46→51 · De Ketelaere 53→58 | Esposito Se. 23 · Lontani 7 |
| A/Pc | **Kean 93→102** · Ramos G. 116→125 | Davis K. 65→72 (1° rig.) · Scamacca 57→63 | Colombo 30 · Tourè E. 20 · Adams A. 20 · Geubbels 12 |

**Regola d'oro:** se l'A di uno slot supera il tetto, lascialo andare e aspetta la B o la Value. In un'asta random usciranno.

---

## 4. Rosa tipo: prova che il piano sta nei 500 crediti

Non è una lista della spesa: dimostra che il piano è sostenibile. Prezzi = mercato stimato.

- **XI (367 cr):** Carnesecchi · Vojvoda, Pavlovic, Ostigard, Miranda J. · Calò, Da Cunha · Politano, Vlasic, Berardi · Davis K.
- **Panchina (133 cr, 14 giocatori):** Milinkovic-Savic V. · Theate, Comuzzo, Bellanova, Gallo, Van Der Brempt, Veiga D. · Busio, Fazzini, Adzic · Schmid, Lontani · Tourè E., Geubbels
- **Totale:** 25 giocatori, 500 crediti.

**Soglie operative**
- **XI entro 370-390 crediti.** Oltre i 400 la panchina scende a 1-2 crediti a testa.
- **Ripartizione della rosa tipo:**

| Reparto | Crediti | Quota |
|---|---|---|
| Por | 41 | 8% |
| Difesa | 112 | 22% |
| Centrocampo | 106 | 21% |
| Trequarti | 75 | 15% |
| Attacco | 166 | 33% |

  Da qui il profilo **"Pinta 4-2-3-1"**: Por 7 · Difesa 20 · Centrocampo 20 · Trequarti 20 · Attacco 33.

---

## 5. Se nella checklist cambiate qualcosa

| Scelta | Cosa cambiare nell'app |
|---|---|
| Modulo 4-3-1-2 | Profilo **Pinta 4-3-1-2** (Centrocampo 24, Attacco 35). Due Pc titolari (es. Kean + Colombo), un solo T. Minimi: T 2, Pc 4 |
| Modulo 4-3-3 | Profilo **Pinta 4-3-3**. Servono due W/A (Diao, Berardi, Dybala, Laurientè), T meno importante |
| Modulo 3-4-2-1 | Profilo **Equilibrato**. Minimi: Dc 5, E 3. Obiettivi E: Wesley, Molina N., Saelemaekers, Moreira (costosi) |
| Stella Sì | Tetto **45%**, profilo **Stella**. Il resto a titolari low cost con rigori: Calò, Busio, Schmid, Ostigard, Valeri, Tourè E. |
| Calhanoglu | Profilo **Bonus centrocampo**, tetto 30%. Slot M = Calhanoglu, poi niente De Bruyne o Pulisic: T value (Vlasic, Adzic) |
| Svilar | Tetto portiere fino a 55. Il 2° portiere a 1-8 crediti (Milinkovic-Savic V.) |
| MUST con prezzo alto | Ogni MUST non ancora uscito abbassa l'offerta massima sugli altri. Oltre 125 crediti totali, togliete un obiettivo A dal reparto del MUST |

---

## 6. Configurazione proposta (file pronti)

### `data/config.json`
- **Impostazioni iniziali:** budget 500, tetto 25, stile Normale, riserva 30, target 27, **profiloBudget "Pinta 4-2-3-1"**.
- **Nuovi profili:** Pinta 4-2-3-1, Pinta 4-3-1-2, Pinta 4-3-3. Equilibrato, Stella e Bonus centrocampo restano.
- **minimiRuolo:** Por 2 · Dc 4 · B 0 · Dd 2 · Ds 2 · **E 0** · M 3 · C 3 · W 2 · **T 3** · A 2 · Pc 3.
- **evita:** Douvikas (ballottaggio con Kean), Esposito F.P. (alternativa a Thuram, prezzo gonfiato), Castro S. (chiuso da Malen), Varela G. (hype e infortunio). Juventus e Lazio restano "ultima spiaggia" in automatico.
- **must:** vuoto, da riempire con Ric.

### `data/shortlist.json`
70 righe `[slot, piano, nome]` per i 10 slot del 4-2-3-1. Tutti i nomi sono verificati nel listone.

Validazione eseguita caricando i due file nella v2.7.1: nessun avviso dati, 70 righe shortlist, profilo "Pinta 4-2-3-1" attivo, 0 errori JavaScript.

---

## 7. Come metterla dentro (dopo l'ok di Ric)

1. **GitHub, branch `main`:** carica `data/config.json` e `data/shortlist.json` (sostituisci). Se avete MUST o altri evita, scriveteli in `config.json` prima del commit. Attendi 1-2 minuti e ricarica l'app.
2. **App > Impostazioni.** Lo stato già salvato conserva le impostazioni vecchie, quindi vanno reimpostate a mano:
   - Distribuzione budget → **Pinta 4-2-3-1**;
   - tetto 25, stile Normale, riserva 30 (o quanto deciso).
3. **App > Obiettivi > "Ricarica MUST/evita da config"**: attiva evita e MUST del file. In alternativa, MUST ed evita si segnano direttamente dalla scheda del giocatore (★ / ⊘).
4. **Controllo finale in Obiettivi:** la shortlist per slot compare in fondo; la Rosa usa il profilo Pinta per il budget di reparto e i nuovi minimi per il rischio buchi.

Nota: `minimiRuolo`, profili e shortlist si leggono dai file a ogni apertura. Tetto, stile, riserva e profilo scelto invece stanno nello stato salvato: per questo il passo 2 serve.
