from flask import Flask, render_template_string, render_template, jsonify, url_for
from flask import Flask, render_template, request, redirect
from flask import json
from urllib.request import urlopen
import sqlite3
import traceback

app = Flask(__name__) #creating flask app name

@app.route('/')
def home():
    return render_template("index.html")
    
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    try:
        if request.method == 'POST':
            # Récupérer les données du formulaire
            email = request.form['email']
            message = request.form['message']

            # Insérer les données dans la base de données
            with sqlite3.connect('/home/tahon/database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO clients (email, message) VALUES (?, ?)', (email, message))
                conn.commit()

            # Rediriger vers la page de consultation des messages après l'ajout
            return redirect(url_for('ReadBDD'))

        # Si la méthode est GET, simplement rendre le template du formulaire
        return render_template('messages.html')

    except Exception as e:
        print("Une erreur s'est produite : ", str(e))
        print(traceback.format_exc())
        return str(e), 500
@app.route('/resume_1')
def resume_1():
    return render_template("resume_1.html")

@app.route('/resume_2')
def resume_2():
    return render_template("resume_2.html")

@app.route('/resume_template')
def resume_template():
    return render_template("resume_template.html")
# Création d'une nouvelle route pour la lecture de la BDD
@app.route("/consultation/")
def ReadBDD():
    conn = sqlite3.connect('/home/tahon/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data) 




@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('/home/tahon/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/fiche_clientn/<string:nom>')
def Readfichenom(nom):
    conn = sqlite3.connect('/home/tahon/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE nom LIKE ?', (nom,))
    data = cursor.fetchall()
    conn.close()
    
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/search_client', methods=['GET', 'POST'])
def Searchfiche():

    # nom = input("Nom client a chercher: ");
    if request.method == 'POST':
        nom = request.form['nom']
        conn = sqlite3.connect('/home/tahon/database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clients WHERE nom = ?', (nom,))
        data = cursor.fetchall()
        conn.close()
        if data:
            return render_template('read_data.html', data=data)
        else:
            return "No client found with that name."
    else:     
       return "Method not allowed for..."

@app.route('/ajouter_client/', methods=['GET', 'POST'])
def ajouter_client():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']

        # Insérer les données dans la base de données (ici, je suppose que tu as une table 'clients')
        conn = sqlite3.connect('/home/tahon/database.db')
        cursor = conn.cursor()
        if conn is not None:
            cursor.execute('INSERT INTO clients (nom, prenom, adresse) VALUES (?, ?, ?)', (nom, prenom, adresse))
            conn.commit()
            conn.close()
        else:
            return 'Erreur de connexion à la base de données'

        # Rediriger vers la page de consultation des clients après l'ajout
        return redirect(url_for('/'))

    # Si la méthode est GET, simplement rendre le template du formulaire
    return render_template('create_data.html')

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions (à cacher par la suite)

# Fonction pour créer une entrée "authentifie" dans la session de l'utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/post/<int:post_id>')
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM livres WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    # Si la publication avec l'ID spécifié n'est pas trouvée, renvoie une réponse 404 Not Found
    if post is None:
        return jsonify(error='Post not found'), 404

    # Convertit la publication en un format JSON
    json_post = {'id': post['id'], 'title': post['title'], 'auteur': post['auteur']}
    
    # Renvoie la réponse JSON
    return jsonify(post=json_post)

# Route pour afficher le formulaire de contact
@app.route('/contact')
def contact_form():
    return render_template('contact.html')

if(__name__ == "__main__"):
    app.run()
