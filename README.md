# MedGuard - Central Server

Il **Central Server** del progetto universitario **MedGuard** gestisce l’autenticazione degli utenti e la ricezione dei dati sanitari cifrati dai client.  
Si occupa inoltre di archiviare i dati cifrati e prepararli per l’elaborazione omomorfica, senza mai accedere ai dati in chiaro.

## 🚀 Tecnologie
- **Python 3**
- **Flask** + **Flask-CORS**
- **SQLAlchemy** + **SQLite** per la gestione utenti e dati
- **Paillier** per la cifratura omomorfica
- **Faker** per generare utenti di esempio

## ⚙️ Funzionalità principali
- Creazione automatica del database `medguard.db` se non presente, con utenti di esempio generati casualmente  
- Endpoint di **login** con autenticazione di base e gestione token temporanei  
- Controllo dello stato di **autorizzazione** di un utente tramite hash  
- Ricezione dei **dati cifrati** dai client e salvataggio sia nel database generale sia in struttura per operazioni omomorfiche  
- Restituzione dei dati omomorfici aggregati tramite endpoint dedicato  
- Comunicazione con il Key Server per ottenere token temporanei se l’utente è di tipo “S” (ricercatore)

## ⚙️ Configurazione
- All'avvio del server Flask, il sistema controllerà automaticamente la presenza di un database e ne creerà uno nuovo se non trovato con 10 utenti random già registrati.
- Per accedere al sistema avviare lo script createUser.py, inserire le credenziali e scegliere il ruolo del nuovo utente.
- E' possibile generare una serie di entry randomiche usando lo script generator.py, per simulare i dati.

## 📚 Note
Questo backend è stato sviluppato a scopo didattico per simulare la gestione di dati sanitari cifrati e operazioni omomorfiche.
