curl -X POST -H "Content-Type: application/json" -d '{"Athlete_ID":"1", "Sport":"Course à pied","Prenom":"Jean","FamilyName":"Bernard", "Birth_Date":"1995/03/02", "Sex":"M", "Taille":"180"}' https://0d84-92-184-102-148.eu.ngrok.io/identity
sleep 1
curl -X POST -H "Content-Type: application/json" -d '{"Athlete_ID":"1","Date_of_last_competition":"2023/05/20","Date_of_last_training":"2023/05/20", "Muscle_used_in_the_last_workout":"Jambe","Recovery_status":"2", "frequence_training_week":"3"}' https://0d84-92-184-102-148.eu.ngrok.io/sport
sleep 1
curl -X POST -H "Content-Type: application/json" -d '{"Athlete_ID":"1","Date":"2023/05/20","Position":"Genoux", "Intensity":"2", "Injury_status":"80"}' https://0d84-92-184-102-148.eu.ngrok.io/injuries
sleep 1
curl -X POST -H "Content-Type: application/json" -d '{"Athlete_ID":"1","Title":"Cardio","Description":"Entrainement de course", "Date":"2023/05/20", "Duration_time":"90","Intensity_of_last_training":"4"}' https://0d84-92-184-102-148.eu.ngrok.io/trainingstat
sleep 1
curl -X POST -H "Content-Type: application/json" -d '{"Name":"Jacques", "FamilyName":"test","Speciality":"Coach", "Phone_number":"0652945183", "email":"beprojectisen@gmail.com", "NomSportif":"Bernard", "PrenomSportif":"Jean"}' https://0d84-92-184-102-148.eu.ngrok.io/staff
sleep 1
curl -X POST -H "Content-Type: application/json" -d '{"Athlete_ID":"1","Sleep":"8","General_tiredness":"2", "Aches_pains":"2","Mood_stress":"2", "Weight":"65"}' https://0d84-92-184-102-148.eu.ngrok.io/selfeval

