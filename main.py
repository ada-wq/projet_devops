import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

# Chargement des fichiers CSV avec le chemin complet
train = pd.read_csv(r"C:\Users\Mahamat Adam\OneDrive\Documents\Cours 2023-2024\S2\devops\projet_devops\Data\train.csv")
test = pd.read_csv(r"C:\Users\Mahamat Adam\OneDrive\Documents\Cours 2023-2024\S2\devops\projet_devops\Data\test.csv")

def dataprep(data, train_columns=None):
    # Encodage des variables catégorielles
    sexe = pd.get_dummies(data['Sex'], prefix='sex')
    cabin = pd.get_dummies(data['Cabin'].fillna('X').str[0], prefix='Cabin')
    emb = pd.get_dummies(data['Embarked'].fillna('S'), prefix='emb')
    
    # Remplir l'âge manquant par la moyenne
    age = data['Age'].fillna(data['Age'].mean())
    
    # Normalisation des colonnes Fare et Pclass
    faresc = pd.DataFrame(MinMaxScaler().fit_transform(data[['Fare']].fillna(0)), columns=['Prix'])
    pc = pd.DataFrame(MinMaxScaler().fit_transform(data[['Pclass']]), columns=['Classe'])

    # Combinaison des colonnes finales
    dp = data[['SibSp']].join(pc).join(sexe).join(emb).join(faresc).join(cabin).join(age.rename("Age"))
    
    # Si nous avons des colonnes de train, harmoniser les colonnes
    if train_columns is not None:
        dp = dp.reindex(columns=train_columns, fill_value=0)  # Ajouter les colonnes manquantes avec 0
    return dp

Xtrain = dataprep(train)
Xtest = dataprep(test, train_columns=Xtrain.columns)  # Harmoniser avec les colonnes de l'entraînement

# Harmoniser les colonnes d'entraînement et de test
common_cols = Xtrain.columns.intersection(Xtest.columns)
Xtrain = Xtrain[common_cols]
Xtest = Xtest[common_cols]

# Variables cibles
y = train['Survived']

# Entraînement du modèle RandomForest
rf = RandomForestClassifier(n_estimators=100, random_state=0, max_features=2)
rf.fit(Xtrain, y)

# Évaluation du modèle
score_train = rf.score(Xtrain, y) * 100
print("Score Train -- ", round(score_train, 2), "%")

# Prédictions sur le jeu de test
p_test = rf.predict(Xtest)

# Préparation pour soumission
submission = pd.DataFrame({
    "PassengerId": test["PassengerId"],
    "Survived": p_test
})
submission.to_csv(r"C:\Users\Mahamat Adam\OneDrive\Documents\Cours 2023-2024\S2\devops\projet_devops\Data\submission.csv", index=False)

# Prédire la survie pour un passager donné

# Exemple : Caractéristiques d'un passager (ici, l'ID 892)
passenger_data = {
    'Pclass': [3],
    'Sex': ['male'],
    'Age': [34.5],
    'SibSp': [0],
    'Parch': [0],
    'Fare': [7.8292],
    'Cabin': ['X'],  # Remplacer les valeurs manquantes de Cabin par 'X'
    'Embarked': ['Q']
}

# Créer un DataFrame avec ces caractéristiques
passenger_df = pd.DataFrame(passenger_data)

# Préparer les données pour cette entrée (comme fait avec les données d'entraînement)
Xpassenger = dataprep(passenger_df, train_columns=Xtrain.columns)  # Utiliser les mêmes colonnes que l'entraînement

# Faire la prédiction
survival_prediction = rf.predict(Xpassenger)

# Afficher la prédiction
if survival_prediction == 1:
    print("Le passager a survécu.")
else:
    print("Le passager n'a pas survécu.")
