from datetime import datetime
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)          
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
                                                                                                                               
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm
  
  @app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    # La fonction est fournie, mais vous devez vous assurer que datetime est importé.
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes}) # Utilisée pour le test, mais la logique est utile pour l'API finale.
@app.route('/commits/')
def commit_metrics():
    # 1. Récupération de l'API GitHub
    response = urlopen('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
    raw_content = response.read()
    commits = json.loads(raw_content.decode('utf-8'))
    
    minute_counts = {}
    
    # 2. Traitement des données
    for commit in commits:
        # Indice N°2
        date_string = commit.get('commit', {}).get('author', {}).get('date')
        if date_string:
            # Réutilisation de la logique d'extraction de minute
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
            minute = date_object.minute # La minute est un nombre entre 0 et 59

            # 3. Agrégation (compte le nombre d'occurrences de chaque minute)
            if minute in minute_counts:
                minute_counts[minute] += 1
            else:
                minute_counts[minute] = 1

    # Convertir en format list-of-dicts pour l'affichage JSON
    results = [{'Minute': min, 'Count': count} for min, count in minute_counts.items()]
    return jsonify(results=results)

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")
  

if __name__ == "__main__":
  app.run(debug=True)
