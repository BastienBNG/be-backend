from flask import Flask, request, jsonify
import sqlite3
import time
from prometheus_flask_exporter import PrometheusMetrics
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import requests
import json


app = Flask(__name__)
metrics = PrometheusMetrics(app)

# set the last score value to the metrics
#g = Gauge('Score', 'Last score added')

info = metrics.info('Score', 'Last score added')

load_dotenv()
# Remplir les détails du compte Gmail
MY_ADDRESS = 'bongiornobastien@gmail.com'
PASSWORD = os.getenv('PASSWORD')


#IDENTITE DU SPORTIF

@app.route('/identity', methods=['POST'])
def identity():
    Athlete_ID = request.json['Athlete_ID']
    Sport = request.json['Sport']
    Prenom = request.json['Prenom']
    FamilyName = request.json['FamilyName']
    Birth_Date = request.json['Birth_Date']
    Sex = request.json['Sex']
    Taille = request.json['Taille']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Identity (Athlete_ID, Sport, Prenom, FamilyName, Birth_Date, Sex, Taille) VALUES (?, ?, ?, ?, ?, ?, ?)", (Athlete_ID, Sport, Prenom, FamilyName, Birth_Date, Sex, Taille))
    conn.commit()
    conn.close()

    metrics.counter('users_added', 'Nombre d\'utilisateurs ajoutés à la base de données', labels={'name': Prenom})

    return jsonify({'message': 'Les données de l\'utilisateur ont bien été ajoutées'})

@app.route('/get_identity', methods=['GET'])
def get_identity():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Identity")
    identity = c.fetchall()
    conn.close()

    return jsonify({'Identity': identity})





#SPORT

@app.route('/sport', methods=['POST'])
def sport():
    Athlete_ID = request.json['Athlete_ID']
    Date_of_last_competition = request.json['Date_of_last_competition']
    Date_of_last_training = request.json['Date_of_last_training']
    Muscle_used_in_the_last_workout = request.json['Muscle_used_in_the_last_workout']
    Recovery_status = request.json['Recovery_status']
    frequence_training_week = request.json['frequence_training_week']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Sport (Athlete_ID, Date_of_last_competition, Date_of_last_training, Muscle_used_in_the_last_workout, Recovery_status, frequence_training_week) VALUES (?, ?, ?, ?, ?, ?)", (Athlete_ID, Date_of_last_competition, Date_of_last_training, Muscle_used_in_the_last_workout, Recovery_status, frequence_training_week))
    conn.commit()
    conn.close()

    metrics.counter('sport_added', 'Nombre de\'sport ajoutés à la base de données', labels={'Sport': Date_of_last_competition})

    return jsonify({'message': 'Les données du Sport ont bien été ajoutées'})


@app.route('/get_sport', methods=['GET'])
def get_sport():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Sport")
    Sport = c.fetchall()
    conn.close()

    return jsonify({'Sport': Sport})



# Injuries
@app.route('/injuries', methods=['POST'])
def injuries():
    Athlete_ID = request.json['Athlete_ID']
    Date = request.json['Date']
    Position = request.json['Position']
    Intensity = request.json['Intensity']
    Injury_status = request.json['Injury_status']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Injuries (Athlete_ID, Date, Position, Intensity, Injury_status) VALUES (?, ?, ?, ?, ?)", (Athlete_ID, Date, Position, Intensity, Injury_status))
    conn.commit()
    conn.close()


    return jsonify({'message': 'Les données concernant la dernière blessure ont bien été ajoutées'})


@app.route('/get_injuries', methods=['GET'])
def get_injuries():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Injuries")
    Injury = c.fetchall()
    conn.close()

    return jsonify({'Injury': Injury})

#Training Stat
@app.route('/trainingstat', methods=['POST'])
def trainingstat():
    Athlete_ID = request.json['Athlete_ID']
    Title = request.json['Title']
    Description = request.json['Description']
    Date = request.json['Date']
    Duration_time = request.json['Duration_time']
    Intensity_of_last_training = request.json['Intensity_of_last_training']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Training_stat (Athlete_ID, Title, Description, Date, Duration_time, Intensity_of_last_training) VALUES (?, ?, ?, ?, ?, ?)", (Athlete_ID, Title, Description, Date, Duration_time, Intensity_of_last_training))
    conn.commit()
    conn.close()



    return jsonify({'message': 'Les données concernant le dernier entrainement ont bien été ajoutées'})


@app.route('/get_trainingstat', methods=['GET'])
def get_trainingstat():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Training_stat")
    Training = c.fetchall()
    conn.close()

    return jsonify({'Training': Training})



 #SELFEVALUATION

@app.route('/selfeval', methods=['POST'])
def selfeval():
    Athlete_ID = request.json['Athlete_ID']
    Sleep = request.json['Sleep']
    General_tiredness = request.json['General_tiredness']
    Aches_pains = request.json['Aches_pains']
    Mood_stress = request.json['Mood_stress']
    Weight = request.json['Weight']
    Date = time.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Self_evaluation (Athlete_ID, Sleep, General_tiredness, Aches_pains, Mood_stress, Weight, Date) VALUES (?, ?, ?, ?, ?, ?, ?)", (Athlete_ID, Sleep, General_tiredness, Aches_pains, Mood_stress, Weight, Date))
    conn.commit()
    
    
    c.execute("SELECT * FROM Identity WHERE Athlete_ID = ?", (Athlete_ID))
    Identityjson = c.fetchone()
    columns = [col[0] for col in c.description]
    IdentityDict = dict(zip(columns, Identityjson))
    Identityout = json.dumps(IdentityDict)

    c.execute("SELECT * FROM Sport WHERE Athlete_ID = ?", (Athlete_ID))
    Sportjson = c.fetchone()
    columns = [col[0] for col in c.description]
    SportDict = dict(zip(columns, Sportjson))
    Sportout = json.dumps(SportDict)

    c.execute("SELECT * FROM Self_evaluation WHERE Athlete_ID = ? ORDER BY Date DESC LIMIT 1;", (Athlete_ID))
    Self_evaluationjson = c.fetchone()
    columns = [col[0] for col in c.description]
    Self_evaluationDict = dict(zip(columns, Self_evaluationjson))
    Self_evaluationout = json.dumps(Self_evaluationDict)

    c.execute("SELECT * FROM Injuries WHERE Athlete_ID = ?", (Athlete_ID))
    Injuriesjson = c.fetchone()
    columns = [col[0] for col in c.description]
    InjuriesDict = dict(zip(columns, Injuriesjson))
    Injuriesout = json.dumps(InjuriesDict)

    c.execute("SELECT * FROM Training_stat WHERE Athlete_ID = ?", (Athlete_ID))
    Training_statjson = c.fetchone()
    columns = [col[0] for col in c.description]
    Training_statDict = dict(zip(columns, Training_statjson))
    Training_statout = json.dumps(Training_statDict)
    
    
    
    conn.close()

    json_data = [{
    "Identity":Identityout,
    "Sport":Sportout,
    "Self_evaluation":Self_evaluationout,
    "Injuries":Injuriesout,
    "Training_stat":Training_statout
    }]
    
    
    print(json_data)

    '''
    json_data = [
  {
    "Identity": {
      "Athlete_ID": 101,
      "Sport": "football",
      "Prenom": "John",
      "FamilyName": "Doe",
      "Birth_Date": "1995/03/22",
      "Sex": "M",
      "Taille": 180
    },
    "Sport": {
      "Sport_ID": 201,
      "Athlete_ID": 101,
      "Date_of_last_competition": "2022/02/05",
      "Date_of_last_training": "2022/02/10",
      "Muscle_used_in_the_last_workout": "Jambe",
      "Recovery_status": 7,
      "training_frequency_week":2
    },
    "Self_evaluation": {
      "Athlete_ID": 101,
      "Sleep": 10,
      "General_tiredness": 10,
      "Aches_pains": 10,
      "Mood_stress": 10,
      "Weight": 75
    },
    "Injuries": {
      "Athlete_ID": 101,
      "Date": "2020/02/15",
      "Position": "Poignet",
      "Intensity": 10,
      "injury_status": 30
    },
    "Staff": {
      "Staff_ID": 301,
      "Name": "Julia",
      "FamilyName": "Smith",
      "Speciality": "physiotherapist",
      "Phone_number": 123456789,
      "email": "julia.smith@gmail.com",
      "athlete_id": "101"
    },
    "Training_stat": {
      "Athlete_ID": 101,
      "Title": "Interval training",
      "Description": "High intensity interval training for 30 minutes",
      "Date": "2022/02/12",
      "Duration_time": 5,
      "Intensity_of_last_training": 4
    },
    "Advice": {
      "Staff_ID": 301,
      "Athlete_ID": 101,
      "Date": "2022/02/15",
      "Advice": "Rest for a few days and apply ice to the injured area."
    },
    "Score": {
      "Athlete_ID": 101,
      "Score": 75,
      "Date": "2022/02/14"
    }
  }] '''
  
    #print(json_data)

    # Faire une demande POST à une autre URL
    url = 'http://ia.default.svc.cluster.local:2000/ia'
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, json=json_data, headers=headers)

    return jsonify({'message': 'Les données de votre auto-évaluation ont bien été enregistrées, votre score vas etre mis à jour'})


@app.route('/get_selfeval', methods=['GET'])
def get_selfeval():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Self_evaluation")
    Self_evaluation = c.fetchall()
    conn.close()

    return jsonify({'Self_evaluation': Self_evaluation})

#STAFF

@app.route('/staff', methods=['POST'])
def staff():
    #Staff_ID = request.json['Staff_ID']
    Name = request.json['Name']
    FamilyName = request.json['FamilyName']
    Speciality = request.json['Speciality']
    Phone_number = request.json['Phone_number']
    email = request.json['email']
    NomSportif = request.json['NomSportif']
    PrenomSportif = request.json['PrenomSportif']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    # Exécuter la requête SQL en utilisant des paramètres de requête
    c.execute("SELECT Athlete_ID FROM Identity WHERE FamilyName = ? AND Prenom = ?", (NomSportif, PrenomSportif))
    athlete_id = c.fetchone()[0]

    if athlete_id:
        c.execute("INSERT INTO Staff (Name, FamilyName, Speciality, Phone_number, email, athlete_id) VALUES (?, ?, ?, ?, ?, ?)", (Name, FamilyName, Speciality, Phone_number, email, athlete_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Les données du staff ont bien été ajoutées'})
    else:
        conn.close()
        return jsonify({'message': 'Le nom ou le prénom n\'existe pas'})


    


@app.route('/get_staff', methods=['GET'])
def get_staff():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Staff")
    Staff = c.fetchall()
    conn.close()

    return jsonify({'Staff': Staff})


#ADVICE

@app.route('/advice', methods=['POST'])
def advice():
    Staff_ID = request.json['Staff_ID']
    Athlete_ID = request.json['Athlete_ID']
    Date = request.json['Date']
    Advice = request.json['Advice']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Advice (Staff_ID, Athlete_ID, Date, Advice) VALUES (?, ?, ?, ?)", (Staff_ID, Athlete_ID, Date, Advice))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Les conseils ont bien été ajoutées'})


@app.route('/get_advice', methods=['GET'])
def get_advice():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Advice")
    Advice = c.fetchall()
    conn.close()

    return jsonify({'Advice': Advice})

#SCORE

@app.route('/score', methods=['POST'])
def score():
    Athlete_ID = request.json['Athlete_ID']
    Score = request.json['Score']
    Date = time.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Score (Athlete_ID, Score, Date) VALUES (?, ?, ?)", (Athlete_ID, Score, Date))
    conn.commit()
    # retrieve the last score value from the database
    c.execute("SELECT Score FROM Score ORDER BY Date DESC LIMIT 1")
    last_score = c.fetchone()[0]
    c.execute("SELECT email FROM Staff WHERE athlete_id = ?", (Athlete_ID,))
    email = c.fetchone()[0]
    c.execute("SELECT Prenom FROM Identity WHERE athlete_id = ?", (Athlete_ID,))
    prenom = c.fetchone()[0]
    c.execute("SELECT FamilyName FROM Identity WHERE athlete_id = ?", (Athlete_ID,))
    nom = c.fetchone()[0]

    last_score_entier = int(last_score)
    conn.close()

    #Si le score est supérieur à 50 alors envoie de mail
    if last_score_entier > 50:
        # Définir les détails du message
        msg = MIMEMultipart()
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Attention ! Votre sportif vient d\'atteindre une valeur de fatigue critique !'

        body = "Bonjour,\nNous avons estimé que le sportif " + prenom + " " + nom + " a atteint une valeur critique de fatigue. \nCette valeur est de " + str(last_score_entier) + "\nVeuillez prendre les mesures necessaires pour éviter toutes blessures."
        msg.attach(MIMEText(body, 'plain'))

        #Connexion au serveur Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(MY_ADDRESS, PASSWORD)

        # Envoyer l'email
        text = msg.as_string()
        server.sendmail(MY_ADDRESS, email, text)

        # Fermer la connexion au serveur
        server.quit()
    

    info.set(last_score)
    #metrics.gauge('last_score', 'Last user score')(last_score)
    #metric_name = 'Score'
    #metrics.info(metric_name, 'Last user score', value=last_score)

    return jsonify({'message': 'Les données concernant le dernier score ont bien été ajoutées'})


@app.route('/get_score', methods=['GET'])
def get_score():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Score")
    Score = c.fetchall()
    conn.close()

    return jsonify({'Score': Score})



if __name__ == '__main__':
    app.run('0.0.0.0', 8080)

