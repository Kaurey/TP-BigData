# TP Big Data

Ce projet implémente une architecture Big Data complète de bout en bout ("End-to-End"), de l'ingestion à la visualisation.

## Architecture

1.  **Sources de Données** :
    *   **CSV** : Transactions de ventes (`data/raw/transactions.csv`).
    *   **JSON** : Logs d'événements utilisateurs (`data/raw/events.json`).
    *   **PostgreSQL** : Base de données utilisateurs (Table `users`).

2.  **Infrastructure (Docker)** :
    *   `postgres` : Serveur de base de données relationnelle.
    *   `spark`: Conteneur Python/Spark qui exécute le job de traitement.
    *   `streamlit`: Conteneur Streamlit pour la visualisation.

3.  **Pipeline de Données (Spark)** :
    *   **Bronze** : Copie brute des données sources au format Parquet.
    *   **Silver** : Nettoyage, typage, et jointure (Transactions + Utilisateurs).
    *   **Gold** : Agrégations (Ventes par pays, ventes quotidiennes, distribution des événements).

4.  **Visualisation** :
    *   Tableau de bord interactif affichant les KPIs de la couche Gold.

## Comment Lancer le Projet

### Pré-requis
*   Docker Desktop installé et lancé.

### Instructions

1.  Ouvrez un terminal dans ce dossier.
2.  Construisez et lancez les conteneurs :
    ```bash
    docker-compose up --build
    ```
3.  Attendez que les services démarrent.
    *   Le service `spark` va s'exécuter, traiter les données, puis s'arrêter (code 0).
    *   Une fois les données prêtes, accédez au Dashboard.

4.  Accédez à l'application de visualisation :
    *   Ouvrez votre navigateur : **http://localhost:8501**

## Structure des Dossiers

*   `data/` : Contient les données (raw, bronze, silver, gold).
*   `src/` : Scripts Python (`etl.py`, `app.py`).
*   `postgres_init/` : Script d'initialisation SQL.

## Lien du diaporama

https://gamma.app/docs/TP-Architecture-Big-Data-r4vkhda19k23h7a?mode=doc
