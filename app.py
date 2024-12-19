import pandas as pd
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler

# Charger les fichiers CSV
train = pd.read_csv('Data/train.csv')
test = pd.read_csv('Data/test.csv')

# Fonction de préparation des données
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

    # Harmoniser avec les colonnes de l'entraînement
    if train_columns is not None:
        dp = dp.reindex(columns=train_columns, fill_value=0)  # Ajouter les colonnes manquantes avec 0
    return dp

# Préparation des données et modèle
Xtrain = dataprep(train)
Xtest = dataprep(test, train_columns=Xtrain.columns)

# Harmoniser les colonnes d'entraînement et de test
common_cols = Xtrain.columns.intersection(Xtest.columns)
Xtrain = Xtrain[common_cols]
Xtest = Xtest[common_cols]

# Variables cibles
y = train['Survived']

# Entraînement du modèle RandomForest
rf = RandomForestClassifier(n_estimators=100, random_state=0, max_features=2)
rf.fit(Xtrain, y)

# Fonction de prédiction pour un passager
def predict_passenger(pclass, sex, age, sibsp, parch, fare, cabin, embarked):
    # Données du passager
    passenger_data = {
        'Pclass': [pclass],
        'Sex': [sex],
        'Age': [age],
        'SibSp': [sibsp],
        'Parch': [parch],
        'Fare': [fare],
        'Cabin': [cabin],  # Remplacer les valeurs manquantes de Cabin par 'X'
        'Embarked': [embarked]
    }

    # Créer un DataFrame avec ces caractéristiques
    passenger_df = pd.DataFrame(passenger_data)

    # Préparer les données pour cette entrée (comme fait avec les données d'entraînement)
    Xpassenger = dataprep(passenger_df, train_columns=Xtrain.columns)  # Utiliser les mêmes colonnes que l'entraînement

    # Faire la prédiction
    survival_prediction = rf.predict(Xpassenger)

    # Retourner la prédiction
    return "Le passager a survécu." if survival_prediction == 1 else "Le passager n'a pas survécu."


# Initialiser l'application Flask
app = Flask(__name__)

# Route pour tester que l'API fonctionne
@app.route('/')
def home():
    return "API de prédiction de survie Titanic en ligne"

# Route pour prédire la survie d'un passager
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données envoyées par l'utilisateur
        data = request.get_json()  # On attend un JSON dans la requête POST

        # Extraire les informations du passager depuis le JSON
        pclass = int(data['pclass'])
        sex = data['sex'].lower()
        age = float(data['age'])
        sibsp = int(data['sibsp'])
        parch = int(data['parch'])
        fare = float(data['fare'])
        cabin = data['cabin']
        embarked = data['embarked'].upper()

        # Faire la prédiction en utilisant la fonction déjà définie
        result = predict_passenger(pclass, sex, age, sibsp, parch, fare, cabin, embarked)

        # Retourner la réponse sous forme de JSON
        return jsonify({'prediction': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



