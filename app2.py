from flask import Flask, request, jsonify
import sqlite3
import time
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Gauge


app = Flask(__name__)
metrics = PrometheusMetrics(app)


# set the last score value to the metrics
g = Gauge('Score', 'Last score added')


#IDENTITE DU SPORTIF

@app.route('/identity', methods=['POST'])
def identity():
    Sport = request.json['Sport']
    Prenom = request.json['Prenom']
    FamilyName = request.json['FamilyName']
    Birth_Date = request.json['Birth_Date']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Identity (Sport, Prenom, FamilyName, Birth_Date) VALUES (?, ?, ?, ?)", (Sport, Prenom, FamilyName, Birth_Date))
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

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO Staff (Staff_ID, Name, FamilyName, Speciality, Phone_number) VALUES (?, ?, ?, ?, ?)", (Staff_ID, Name, FamilyName, Speciality, Phone_number))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Staff stats added successfully'})


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
    print(last_score)


    conn.close()


    

    g.set(last_score)
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

