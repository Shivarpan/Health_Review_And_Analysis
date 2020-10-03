# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging 
from bs4 import BeautifulSoup
import requests
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort
from jinja2              import TemplateNotFound
import csv

# App modules
from app        import app, lm, db, bc
from app.models import User
from app.forms  import LoginForm, RegisterForm
import app.diseaseprediction as di

symptoms = ['itching',
 'skin_rash',
 'nodal_skin_eruptions',
 'continuous_sneezing',
 'shivering',
 'chills',
 'joint_pain',
 'stomach_pain',
 'acidity',
 'ulcers_on_tongue',
 'muscle_wasting',
 'vomiting',
 'burning_micturition',
 'spotting_ urination',
 'fatigue',
 'weight_gain',
 'anxiety',
 'cold_hands_and_feets',
 'mood_swings',
 'weight_loss',
 'restlessness',
 'lethargy',
 'patches_in_throat',
 'irregular_sugar_level',
 'cough',
 'high_fever',
 'sunken_eyes',
 'breathlessness',
 'sweating',
 'dehydration',
 'indigestion',
 'headache',
 'yellowish_skin',
 'dark_urine',
 'nausea',
 'loss_of_appetite',
 'pain_behind_the_eyes',
 'back_pain',
 'constipation',
 'abdominal_pain',
 'diarrhoea',
 'mild_fever',
 'yellow_urine',
 'yellowing_of_eyes',
 'acute_liver_failure',
 'fluid_overload',
 'swelling_of_stomach',
 'swelled_lymph_nodes',
 'malaise',
 'blurred_and_distorted_vision',
 'phlegm',
 'throat_irritation',
 'redness_of_eyes',
 'sinus_pressure',
 'runny_nose',
 'congestion',
 'chest_pain',
 'weakness_in_limbs',
 'fast_heart_rate',
 'pain_during_bowel_movements',
 'pain_in_anal_region',
 'bloody_stool',
 'irritation_in_anus',
 'neck_pain',
 'dizziness',
 'cramps',
 'bruising',
 'obesity',
 'swollen_legs',
 'swollen_blood_vessels',
 'puffy_face_and_eyes',
 'enlarged_thyroid',
 'brittle_nails',
 'swollen_extremeties',
 'excessive_hunger',
 'extra_marital_contacts',
 'drying_and_tingling_lips',
 'slurred_speech',
 'knee_pain',
 'hip_joint_pain',
 'muscle_weakness',
 'stiff_neck',
 'swelling_joints',
 'movement_stiffness',
 'spinning_movements',
 'loss_of_balance',
 'unsteadiness',
 'weakness_of_one_body_side',
 'loss_of_smell',
 'bladder_discomfort',
 'foul_smell_of urine',
 'continuous_feel_of_urine',
 'passage_of_gases',
 'internal_itching',
 'toxic_look_(typhos)',
 'depression',
 'irritability',
 'muscle_pain',
 'altered_sensorium',
 'red_spots_over_body',
 'belly_pain',
 'abnormal_menstruation',
 'dischromic _patches',
 'watering_from_eyes',
 'increased_appetite',
 'polyuria',
 'family_history',
 'mucoid_sputum',
 'rusty_sputum',
 'lack_of_concentration',
 'visual_disturbances',
 'receiving_blood_transfusion',
 'receiving_unsterile_injections',
 'coma',
 'stomach_bleeding',
 'distention_of_abdomen',
 'history_of_alcohol_consumption',
 'fluid_overload.1',
 'blood_in_sputum',
 'prominent_veins_on_calf',
 'palpitations',
 'painful_walking',
 'pus_filled_pimples',
 'blackheads',
 'scurring',
 'skin_peeling',
 'silver_like_dusting',
 'small_dents_in_nails',
 'inflammatory_nails',
 'blister',
 'red_sore_around_nose',
 'yellow_crust_ooze',
 'prognosis']

symptoms.sort()

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template( 'accounts/register.html', form=form, msg=msg )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template( 'accounts/register.html', form=form, msg=msg )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unknown user"

    return render_template( 'accounts/login.html', form=form, msg=msg )

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    try:

        if not path.endswith( '.html' ):
            path += '.html'

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Return sitemap
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')


@app.route('/dummy.html', methods=['GET', 'POST'])
def dummy():
    return render_template("dummy.html", symptoms=symptoms)

def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def output():
    r = sr.Recognizer()
    text = ""

    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        # listen for 5 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=1)
        print("Speak Anything")
        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            print("You said: {}".format(text))

        except:
            print("Sorry could not recognize your voice.")
        
        return text


@app.route('/predict.html', methods=['GET','POST'])
def predict():
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])

    

    if(request.form["form"] == "decision"):
        ran = di.decision_tree(selected_symptoms)
        svm_ = di.randomforest(selected_symptoms)
        nai = di.NaiveBayes(selected_symptoms)
        log = di.logistic_reg(selected_symptoms)
        dis = di.svm_(selected_symptoms)
        lis = [dis, ran, nai,log,svm_]
        count = 0
        for i in lis:
            if i == dis:
                count+=1
        per = (count/5)*100
        per = round(per,2)
        # selected_symptoms.append(per)
        # dis = disease.replace('_', " ")
        source = requests.get(f"https://www.nhsinform.scot/search?q={dis}&locpt=&ds=&tab=inform").text
        soup = BeautifulSoup(source, 'lxml')

        disease = soup.ol.a['href']

        source1 = requests.get(f"https://www.nhsinform.scot{disease}").text
        soup = BeautifulSoup(source1, 'lxml')

        desc = soup.find('div', class_="editor").p.text
        web_link = f"https://www.nhsinform.scot{disease}"
        
        return render_template(url_for('predict'),disease=dis,symp=selected_symptoms, desc = desc, per=per, lin = web_link, symptoms=symptoms)
    
    
    if (request.form['form'] == 'play'):
        speak("Hi, Please tell us the symptoms")
        text = output()
        speak("Thank You!")
        print(text)
        text = text.split()
        symp = []
        for tex in text:
            if tex in symptoms:
                symp.append(tex)
        
        # symp = symp[:5]
        
        # dis = di.decision_tree(symp)
        ran = di.decision_tree(symp)
        dis = di.randomforest(symp)
        nai = di.NaiveBayes(symp)
        log = di.logistic_reg(symp)
        svm_ = di.svm_(symp)
        lis = [dis, ran, nai, log, svm_]
        count = 0
        for i in lis:
            if i == dis:
                count+=1
        per = (count/5)*100
        per = round(per,2)
        # dis = disease.replace('_', " ")
        source = requests.get(f"https://www.nhsinform.scot/search?q={dis}&locpt=&ds=&tab=inform").text
        soup = BeautifulSoup(source, 'lxml')
        with open("debug.txt", 'w') as file:
            file.write(soup.prettify())

        disease = soup.ol.a['href']

        source1 = requests.get(f"https://www.nhsinform.scot{disease}").text
        soup = BeautifulSoup(source1, 'lxml')

        desc = soup.find('div', class_="editor").p.text
        web_link = f"https://www.nhsinform.scot{disease}"

        return render_template(url_for('predict'),disease=svm_,symp=symp,per=per, desc = desc, lin = web_link, symptoms=symptoms)

@app.route('/covidInfo.html', methods=['GET','POST'])
def covidInfo():
    source=requests.get(f"https://www.mohfw.gov.in/").text
    soup = BeautifulSoup(source, 'lxml')

    state_all = soup.find_all('tr')[0:-4]

    state_list = []
    state = []
    for i in range(6):
	    state.append(state_all[0].find_all('th')[i].text)

    state_list.append(state)

    for i in range(1,len(state_all)):
	    state = []
	    for k in range(6):
		    state.append(state_all[i].find_all('td')[k].text)

	    state_list.append(state)

    return render_template('covidInfo.html', state_list=state_list)