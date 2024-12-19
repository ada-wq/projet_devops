# README - Projet MLOps : Déploiement Automatisé d'une Solution ML

## 1. Introduction

Le projet **MLOps - Déploiement automatisé d'une solution ML** repose sur l'utilisation du modèle **Titanic Survival** pour prédire la survie des passagers du Titanic. Ce guide détaille toutes les étapes pour configurer et déployer une application ML avec un pipeline complet d'intégration et de déploiement continu (CI/CD), utilisant des outils comme Docker, Terraform, Ansible et GitHub Actions.

---

## 2. Structure du Projet

L'organisation des répertoires et fichiers du projet est la suivante :

```
projet_devops/
├── Data/
│   ├── train.csv
│   ├── test.csv
├── Dockerfile
├── app.py
├── predict_survival.py
├── main.py
├── requirements.txt
├── terraform/
│   ├── main.tf
├── ansible/
│   ├── playbook.yml
├── .github/
│   ├── workflows/
│   │   ├── ci_cd.yml
├── README.md
└── docs/
    ├── Doc_projet_devops.docx
```

---

## 3. Code des Fichiers

### 3.1 `app.py`

Ce fichier contient l'API Flask pour prédire la survie des passagers du Titanic. L'API prend en entrée des informations sur un passager et renvoie une prédiction de survie. Voici les points clés :

- **Chargement des données** : Les fichiers `train.csv` et `test.csv` sont chargés dans Pandas pour l'analyse.
- **Prétraitement des données** : La fonction `dataprep` prépare les données pour la prédiction (encodage des variables catégorielles, mise à l'échelle des valeurs numériques).
- **Modèle** : Un modèle RandomForestClassifier est entraîné sur les données d'entraînement.
- **Endpoints Flask** : Un endpoint `/predict` permet de prédire la survie d'un passager via une requête HTTP POST.

### 3.2 `Dockerfile`

Le `Dockerfile` permet de conteneuriser l'application Flask. Il inclut les étapes suivantes :

1. **Image de base** : Utilisation de `python:3.9-slim`.
2. **Installation des dépendances** : Installe les dépendances définies dans `requirements.txt`.
3. **Exécution de l'application** : Le conteneur lance l'application Flask avec `CMD ["python", "app.py"]`.

### 3.3 `main.py`

Ce fichier est responsable de l'entraînement du modèle Titanic Survival en utilisant un modèle `RandomForestClassifier`. Il inclut :

- **Préparation des données** : Transformation des variables et normalisation des valeurs.
- **Entraînement du modèle** : Le modèle est entraîné sur les données d'entraînement et évalué sur les données de test.
- **Prédictions** : Génération des prédictions sur le jeu de données de test et création du fichier `submission.csv`.

### 3.4 `requirements.txt`

Ce fichier contient toutes les dépendances Python nécessaires pour l'exécution du projet :

```txt
flask
pandas
scikit-learn
numpy
```

### 3.5 `terraform/main.tf`

Ce fichier contient la configuration Terraform pour déployer l'infrastructure dans AWS. Il inclut :

- **Configuration AWS** : Utilisation de la région `us-west-2`.
- **Création d'une instance EC2** : Déploiement d'une instance EC2 avec l'AMI et le type spécifiés.
- **Sortie de l'IP publique** : Affichage de l'adresse IP publique de l'instance EC2.

### 3.6 `ansible/playbook.yml`

Ce fichier est un playbook Ansible pour configurer le serveur de machine learning. Il inclut les tâches suivantes :

1. **Installation de Python** : Installation de Python3 sur le serveur.
2. **Installation des packages Python** : Installation des dépendances nécessaires via `pip`.

### 3.7 GitHub Actions (`.github/workflows/ci_cd.yml`)

Ce fichier définit un pipeline CI/CD avec GitHub Actions. Il inclut les étapes suivantes :

1. **Clonage du code** : Récupération du code source du projet.
2. **Installation des dépendances** : Installation de Python et des packages nécessaires.
3. **Construction de l'image Docker** : Création de l'image Docker pour l'application Flask.
4. **Tests** : Exécution des tests unitaires avec `pytest`.
5. **Déploiement** : Déploiement de l'application Docker sur un serveur.

---

## 4. Étapes d'Exécution

### 4.1 Préparation du Projet

1. **Cloner le projet** : Clonez le projet depuis GitHub ou créez le répertoire localement.
2. **Ajouter les données** : Assurez-vous que les fichiers `train.csv` et `test.csv` sont placés dans le répertoire `Data/`.
3. **Installer Docker et Terraform** : Assurez-vous que Docker et Terraform sont installés sur votre machine.

### 4.2 Construire et Déployer l'Application

1. **Construire l'image Docker** :
   Exécutez la commande suivante pour construire l'image Docker à partir du `Dockerfile` :
   
   ```bash
   docker build -t titanic_model .
   ```

2. **Lancer l'application Flask** :
   Lancez l'application Flask dans un conteneur Docker :
   
   ```bash
   docker run -d -p 5000:5000 titanic_model
   ```

3. **Tester l'API** :
   Vous pouvez tester l'API en utilisant des outils comme `Postman` ou `curl`. Voici un exemple de requête `curl` :

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
       "pclass": 3, 
       "sex": "male", 
       "age": 22, 
       "sibsp": 0, 
       "parch": 0, 
       "fare": 7.25, 
       "cabin": "X", 
       "embarked": "S"
   }' http://localhost:5000/predict
   ```

### 4.3 Déploiement avec Terraform et Ansible

1. **Terraform** : Déployez l'infrastructure AWS en exécutant les commandes suivantes :
   
   ```bash
   terraform init
   terraform apply
   ```

2. **Ansible** : Configurez les serveurs et installez les dépendances nécessaires en utilisant Ansible :

   ```bash
   ansible-playbook ansible/playbook.yml
   ```

---

## 5. Conclusion

Le projet MLOps permet de créer une solution de prédiction de survie des passagers du Titanic en utilisant Flask pour l'API, Docker pour la conteneurisation, Terraform pour l'infrastructure AWS, et Ansible pour la configuration des serveurs. Ce pipeline CI/CD assure une automatisation complète de l'intégration et du déploiement, facilitant ainsi la gestion de modèles ML en production.

N'oubliez pas de bien gérer vos secrets (par exemple via AWS Secrets Manager) et d'optimiser le modèle pour une mise en production réussie.

---

## 6. Documentation

Une documentation détaillée sur le projet est également disponible dans le fichier `docs/Doc_projet_devops.docx`.

