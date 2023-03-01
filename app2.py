from flask import Flask, request, jsonify
import sqlite3
import time
from prometheus_flask_exporter import PrometheusMetrics
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv


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

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Identity (Athlete_ID, Sport, Prenom, FamilyName, Birth_Date) VALUES (?, ?, ?, ?, ?)", (Athlete_ID, Sport, Prenom, FamilyName, Birth_Date))
    conn.commit()
    conn.close()

    metrics.counter('users_added', 'Nombre d\'utilisateurs ajoutés à la base de données', labels={'name': Prenom})

    return jsonify({'message': 'User added successfully'})

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

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Sport (Athlete_ID, Date_of_last_competition, Date_of_last_training, Muscle_used_in_the_last_workout, Recovery_status) VALUES (?, ?, ?, ?, ?)", (Athlete_ID, Date_of_last_competition, Date_of_last_training, Muscle_used_in_the_last_workout, Recovery_status))
    conn.commit()
    conn.close()

    metrics.counter('sport_added', 'Nombre de\'sport ajoutés à la base de données', labels={'Sport': Date_of_last_competition})

    return jsonify({'message': 'Sport stats added successfully'})


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

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Injuries (Athlete_ID, Date, Position, Intensity) VALUES (?, ?, ?, ?)", (Athlete_ID, Date, Position, Intensity))
    conn.commit()
    conn.close()


    return jsonify({'message': 'Injury stats added successfully'})


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



    return jsonify({'message': 'Training stats added successfully'})


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

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Self_evaluation (Athlete_ID, Sleep, General_tiredness, Aches_pains, Mood_stress, Weight) VALUES (?, ?, ?, ?, ?, ?)", (Athlete_ID, Sleep, General_tiredness, Aches_pains, Mood_stress, Weight))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Self evaluation stats added successfully'})


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
    Staff_ID = request.json['Staff_ID']
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
        c.execute("INSERT INTO Staff (Staff_ID, Name, FamilyName, Speciality, Phone_number, email, athlete_id) VALUES (?, ?, ?, ?, ?, ?, ?)", (Staff_ID, Name, FamilyName, Speciality, Phone_number, email, athlete_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Staff stats added successfully'})
    else:
        return jsonify({'message': 'Mauvais Nom ou Prénom'})

    


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

    return jsonify({'message': 'Advice stats added successfully'})


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


    conn.close()

    #Si le score est supérieur à 7 alors envoie de mail
    if last_score > 7:
        # Définir les détails du message
        msg = MIMEMultipart()
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = 'Attention ! Votre sportif vient d\'atteindre une valeur de fatigue critique !'

        body = "Bonjour,\nNous avons estimé que le sportif " + prenom + " " + nom + " a atteint une valeur critique de fatigue. \nCette valeur est de " + str(last_score) + "\nVeuillez prendre les mesures necessaires pour éviter toutes blessures."
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

    return jsonify({'message': 'Score stats added successfully'})


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

