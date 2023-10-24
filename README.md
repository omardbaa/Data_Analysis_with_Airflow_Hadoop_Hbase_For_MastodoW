# Data_Analysis_with_Airflow_Hadoop_Hbase_For_Mastodon

# Mastodon Data Pipeline

![GitHub](https://img.shields.io/github/license/omardbaa/Data_Analysis_with_Airflow_Hadoop_Hbase_For_MastodoW) ![GitHub dernière validation](https://img.shields.io/github/last-commit/omardbaa/Data_Analysis_with_Airflow_Hadoop_Hbase_For_MastodoW) ![GitHub problèmes](https://img.shields.io/github/issues/omardbaa/Data_Analysis_with_Airflow_Hadoop_Hbase_For_MastodoW)

Data_Analysis_with_Airflow_Hadoop_Hbase_For_Mastodon est un projet de pipeline de données composé de quatre phases principales : extraction de données à partir de l'API Mastodon, traitement des données avec Hadoop MapReduce en utilisant Python en streaming, stockage des données dans HBase et orchestration avec Apache Airflow pour une exécution automatisée quotidienne. Le projet vise à collecter et analyser des données de la plateforme Mastodon, une plateforme de médias sociaux fédérée.

## Aperçu du Projet

### Phase 1: Collecte de Données
- 📡 **Extraction de Données :** Utilisez l'API Mastodon avec vos jetons d'accès pour collecter des données brutes depuis la plateforme Mastodon.

- 💾 **Stockage des Données Brutes :** Stockez les données brutes dans un système de fichiers distribué tel que HDFS pour garantir la scalabilité.

- 🗄️ **Modélisation du Data Lake HDFS :** Définissez le schéma du data lake pour HDFS.

### Phase 2: Traitement de Données avec MapReduce
- 🗺️ **Mappeur :** Traitez les données d'entrée et générez des paires clé-valeur en fonction des métriques souhaitées (par exemple, les abonnés des utilisateurs, le taux d'engagement, les URL, les emojis, etc.).

- 📊 **Réducteur :** Agrégez les paires clé-valeur produites par le mappeur.

- ⚙️ **Exécution du Travail MapReduce :** Utilisez l'API de streaming Hadoop pour exécuter la tâche MapReduce, en fournissant les scripts du mappeur et du réducteur comme entrées.

- 📈 **Surveillance :** Suivez la progression du travail grâce à l'interface web Hadoop.

### Phase 3: Stockage des Données dans HBase
- 🗂️ **Conception du Schéma HBase :** Concevez le schéma HBase en fonction des informations que vous souhaitez extraire.

- ⚖️ **Meilleures Pratiques :** Suivez les meilleures pratiques pour la conception de la clé de ligne, la conception des familles de colonnes, la compression, les filtres de Bloom, les inserts par lot, etc.

- 🏛️ **Création de Tables :** Créez les tables nécessaires dans HBase.

- 📥 **Insertion de Données :** Remplissez les résultats du réducteur dans les tables HBase à l'aide d'un client HBase en Python ou de la méthode de votre choix.

### Phase 4: Orchestration avec Apache Airflow
- 🌪️ **Orchestration du Workflow :** Définissez un graphe acyclique dirigé (DAG) pour orchestrer l'ensemble du workflow.

- 📆 **Création de Tâches :** Créez des tâches pour exécuter le travail MapReduce et stocker les résultats dans HBase.

- 🔍 **Surveillance et Gestion des Erreurs :** Surveillez la progression et gérez les erreurs ou les échecs.

### Phase 5: Analyse de Données
Après avoir réussi les phases précédentes, vous pouvez effectuer l'analyse de données. Vous écrirez des requêtes pour :

#### Analyse des Utilisateurs
- 🧑‍💼 Identifiez les utilisateurs ayant le plus grand nombre d'abonnés.

- 📊 Analysez les taux d'engagement des utilisateurs.

- 📈 Analysez la croissance des utilisateurs au fil du temps en utilisant la métrique `user_created_at`.

#### Analyse du Contenu
- 🔗 Identifiez les sites web externes (URL) les plus partagés.

#### Analyse de la Langue et de la Région
- 🌐 Analysez la distribution des publications en fonction de leur langue.

#### Analyse de l'Engagement des Médias
- 📷 Déterminez le nombre de publications avec des pièces jointes multimédias.

#### Analyse des Balises et des Mentions
- 🏷️ Identifiez les balises et les utilisateurs mentionnés les plus fréquemment utilisés.

### Phase 6: Exécution du Workflow
Dans l'interface web Apache Airflow, activez le DAG, surveillez la progression de l'exécution du DAG et vérifiez les journaux pour tout problème. Une fois le DAG est terminé, examinez les résultats dans HBase.

### Phase 7: Optimisation et Surveillance
- ⚙️ Optimisez les scripts MapReduce pour de meilleures performances. Surveillez HBase pour tout problème de stockage. Configurez des alertes dans Airflow pour les échecs de tâches. Surveillez régulièrement Hadoop en utilisant son interface web respective.

### Phase 8: Mise à Jour de la Configuration des Droits d'Accès
- 🔐 Mettez à jour les jetons d'API si les rôles organisationnels changent, en vous assurant qu'ils ont les autorisations nécessaires pour la récupération de données.

### Phase 9: Mise à Jour de la Documentation
- 📄 Mettez à jour la documentation des règles d'accès, y compris les détails sur les rôles, les autorisations, les demandes d'accès et les procédures d'octroi ou de révocation d'accès.

### Phase 10: Planification et Conformité
## Conformité RGPD dans le Pipeline de Données Mastodon

Pour garantir la conformité au RGPD, notre pipeline de données suit ces étapes essentielles :

1. **Anonymisation des Données :**
   - Suppression ou hachage des données personnelles inutiles.

2. **Minimisation des Données :**
   - Conservation uniquement des données nécessaires à l'analyse.

3. **Sécurité :**
   - Sécurisation des systèmes de stockage HDFS et HBase.

4. **Gestion du Data Lake :**
   - Suppression des données une fois traitées pour éviter la rétention excessive.

5. **Évaluation de l'Impact sur la Protection des Données (AIPD) :**
   - Identification et atténuation des risques pour la vie privée.

6. **Consentement :**
   - Obtention d'un consentement explicite lorsque requis.

7. **Droits des Personnes Concernées :**
   - Possibilité d'accéder, corriger ou supprimer leurs données.

8. **Documentation et Conformité :**
   - Tenue de registres détaillés pour la transparence.

9. **Audits et Vérifications :**
   - Contrôles réguliers de conformité aux réglementations RGPD.

10. **Gestion des Violations de Données :**
    - Protocole de réponse aux violations conforme au RGPD.

Ces mesures démontrent notre engagement envers la conformité au RGPD, la protection des données personnelles et le respect des droits à la vie privée.


## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
