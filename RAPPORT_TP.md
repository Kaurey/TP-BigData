# Rapport de TP : Architecture Big Data de Bout en Bout

**Auteur :** [Votre Nom]
**Date :** Janvier 2026
**Matière :** Big Data

---

## 1. Introduction

Ce rapport présente la conception et l'implémentation d'une architecture Big Data complète ("End-to-End") pour une entreprise fictive. L'objectif était de centraliser des données hétérogènes (fichiers plats et bases relationnelles), de les traiter via un pipeline ETL (Extract, Transform, Load) structuré, et de restituer des indicateurs clés (KPIs) via une interface de visualisation.

## 2. Architecture Technique

Pour répondre aux exigences de robustesse et de scalabilité, nous avons opté pour une architecture conteneurisée basée sur **Docker**.

### Schéma de l'Architecture

Le flux de données suit une architecture en couches ("Medallion Architecture") :

1.  **Sources** :
    *   **Transactions (CSV)** : Données de ventes.
    *   **Événements (JSON)** : Logs d'activité des utilisateurs.
    *   **Utilisateurs (PostgreSQL)** : Données référentielles clients.

2.  **Traitement (Spark)** : Un job Spark unique orchestre le passage des données à travers trois zones :
    *   **Zone Raw/Bronze** : Stockage des données brutes, sans transformation, format Parquet.
    *   **Zone Silver** : Données nettoyées, typées et enrichies (Jointure Ventes + Clients).
    *   **Zone Gold** : Agrégats métier prêts pour l'analyse (Ventes/Pays, Ventes/Jour).

3.  **Visualisation (Streamlit)** : Interface web consommant la zone Gold pour afficher les indicateurs.

### Stack Technologique

*   **Docker & Docker Compose** : Pour l'orchestration et la portabilité de l'environnement.
*   **Apache Spark (PySpark)** : Moteur de traitement distribué pour l'ETL.
*   **PostgreSQL** : Base de données relationnelle source.
*   **Streamlit** : Framework Python pour le dashboarding interactif.
*   **Parquet** : Format de fichier colonnaire optimisé pour le Big Data, utilisé pour le stockage intermédiaire.

## 3. Détail du Pipeline de Données (ETL)

Le script `etl.py` assure le traitement en trois étapes distinctes :

### Phase 1 : Ingestion (Bronze Layer)
L'objectif est de capturer la donnée brute sans perte d'information.
*   Les fichiers CSV et JSON sont lus et convertis en Parquet.
*   La table SQL `users` est extraite via le connecteur JDBC Postgres et sauvegardée en Parquet.
*   *Avantage* : Le format Parquet assure une compression et un typage des données dès le début de la chaîne.

### Phase 2 : Traitement (Silver Layer)
Cette phase nettoie et enrichit les données.
*   **Nettoyage** : Suppression des valeurs nulles et des enregistrements incomplets.
*   **Enrichissement** : Une jointure est effectuée entre les transactions (Ventes) et les utilisateurs (Réferentiel) sur la clé `user_id`. Cela permet d'associer chaque vente à des informations démographiques (Pays, Nom).

### Phase 3 : Agrégations (Gold Layer)
Création de tables analytiques optimisées pour le reporting. Trois indicateurs principaux sont calculés :
1.  **Ventes par Pays** : Somme des montants groupée par pays (`sales_by_country`).
2.  **Tendance des Ventes** : Somme des montants groupée par date (`sales_daily`).
3.  **Distribution des Événements** : Comptage des types d'événements (`view`, `login`, etc.).

## 4. Visualisation des Résultats

L'application `app.py` (Streamlit) lit directement les fichiers de la zone Gold.

Le tableau de bord présente :
*   **KPIs Généraux** : Chiffre d'affaires total, meilleur marché, volume d'événements.
*   **Graphiques** :
    *   Un diagramme en barres montrant la performance par pays.
    *   Un diagramme circulaire ("Pie Chart") pour la répartition des actions utilisateurs.
    *   Une courbe d'évolution temporelle du chiffre d'affaires.

## 5. Conclusion

Ce projet a permis de mettre en œuvre les concepts fondamentaux du Big Data : hétérogénéité des sources, nettoyage de la donnée, et structuration en couches logiques. L'utilisation de Spark garantit que ce pipeline pourrait passer à l'échelle sur des volumétries massives ("Scalabilité"), tandis que Docker assure que l'environnement est reproductible sur n'importe quelle machine.
