

-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/LZooVW
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE Identity (
     Athlete_ID  INTEGER INTEGER PRIMARY KEY,
     Sport  string  NOT NULL ,
     Prenom  string  NOT NULL ,
     FamilyName  string  NOT NULL ,
     Birth_Date  date  NOT NULL ,
     Sex string NOT NULL ,
     Taille int NOT NULL
);



CREATE TABLE  Sport  (
     Athlete_ID  int  NOT NULL ,
     Date_of_last_competition  date  NOT NULL ,
     Date_of_last_training  date  NOT NULL ,
     Muscle_used_in_the_last_workout  string  NOT NULL ,
     Recovery_status  string  NOT NULL ,
     frequence_training_week int
);

CREATE TABLE  Self_evaluation  (
     Athlete_ID  int  NOT NULL ,
     Sleep  string  NOT NULL ,
     General_tiredness  string  NOT NULL ,
     Aches_pains  string  NOT NULL ,
     Mood_stress  string  NOT NULL ,
     Weight  int  NOT NULL ,
     Date date NOT NULL
);

CREATE TABLE  Injuries  (
     Athlete_ID  int  NOT NULL ,
     Date  date  NOT NULL ,
     Position  string  NOT NULL ,
     Intensity  string  NOT NULL ,
     Injury_status int 
     
);

CREATE TABLE  Staff  (
     Staff_ID  INTEGER PRIMARY KEY AUTOINCREMENT ,
     Name  string  NOT NULL ,
     FamilyName  string  NOT NULL ,
     Speciality  string  NOT NULL ,
     Phone_number  varchar  NOT NULL ,
     email string NOT NULL ,
     athlete_id int
    
);

CREATE TABLE  Training_stat  (
     Athlete_ID  int  NOT NULL ,
     Title  string  NOT NULL ,
     Description  string  NOT NULL ,
     Date  date  NOT NULL ,
     Duration_time  string  NOT NULL ,
     Intensity_of_last_training  int  NOT NULL
);

CREATE TABLE  Advice  (
     Athlete_ID  int  NOT NULL ,
     titre  string NOT NULL ,
     description  string  NOT NULL 
);

CREATE TABLE  Score  (
     Athlete_ID int NOT NULL ,
     Score  int  NOT NULL ,
     Date date NOT NULL
);