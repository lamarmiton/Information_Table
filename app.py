# -*- coding: utf-8 -*-
from flask import Flask, flash, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import re
import sqlite3
import pprint as pp
import json
import os
import sys
import shutil
import binascii

#IMPORT DU REPERTOIRE DE SCRIPT PYTHON
sys.path.insert(1,'script/')
from tableIB import parseExcel
from jsonParsing import jsonParsing, jsonToExcel, buildIndic,jsonToExcelAll 

#ENCODAGE UTF8
reload(sys)
sys.setdefaultencoding('utf-8')

# CHEMINS ABSOLUS 
VIEWS_PATH = "static/views/"
JS_PATH = "static/js/"
DB_PATH = "data/"
UPLOAD_FOLDER = "data/Upload"
ALLOWED_EXTENSIONS = set(['xlsx'])



app = Flask(__name__)

#Definition du repertoire d'uploads
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Controller l'extension de fichier
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Configuration de la session Flask
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

# =================================== Index ==================================================================
# ============================================================================================================

# ROUTES    
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("main.html")

# =================================== Affichage de toutes les campagnes ======================================
# ============================================================================================================

#Dans la page campagne, on affiche la liste des campagnes
@app.route('/Campagne', methods=["GET", "POST"])
def campagne():
    # Construction de la requête
    request = '''SELECT DISTINCT * FROM campagne;'''

    # Exécution de la requete et récupération des résultats
    # On souhaite afficher toutes les campagnes
    con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(request)

    rows = cur.fetchall(); 
    con.close()

    return render_template("Campagne.html", rows = rows)

# =================================== Session : Table d'information ==========================================
# ============================================================================================================

#Page de la session : La complétion de l'étude par un répondant
#La creation de la session est lié à la campagne (Retrouvée par son id)
#La session est généré aléatoirement via le fichier Excel de la campagne
@app.route('/Session/<int:campagneId>/', methods=["GET", "POST"])
def session(campagneId):
    try : 

        # Récupération du chemin d'accés vers le fichier Excel de la campagne
        request = 'SELECT Pathfile FROM campagne WHERE id = '+str(campagneId)+';'

        #Recuperation du nom de la campagne 
        requestName = 'SELECT nom FROM campagne WHERE id = '+str(campagneId)+';'

        #Recuperation du countdown de la campagne 
        Requestcountdown = 'SELECT countdown FROM campagne WHERE id = '+str(campagneId)+';'

        #Exécution de la requete et récupération du résultat
        con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(request)

        #Récupération du chemin d'accés vers le fichier Excel
        chemin = str(cur.fetchone()[0])

        cur.execute(requestName)
        name = str(cur.fetchone()[0])

        cur.execute(Requestcountdown)
        countdown = int(cur.fetchone()[0])
        #Enregistrement des changements dans la base de donnée
        con.commit()
        #Fermeture de la base de donnée  
        con.close()

        #Construction du tableau grâce au script python tableIDB.python
        #Le tableau[-1] signifie que l'on prendra toujours le dernier tableau créé
        rows = parseExcel(str(chemin),campagneId).tableau[-1].dic

        return render_template("Session.html",rows = rows, name = name, countdown = countdown)  

    except IOError : 

        print "Error 404 : file not found"
        pass

# =================================== Remove Campagne ========================================================
# ============================================================================================================

#Supression de la campagne : Balayage et ménage des fichiers liés à celle-ci
@app.route('/Delete/<int:campagneid>/', methods=["DELETE","GET"])
def delete(campagneid):
    
    #Ecriture des requetes de supression
    removeSession = 'DELETE FROM session WHERE campagneid = '+str(campagneid)+';'
    removeCampagne = 'DELETE FROM campagne WHERE id = '+str(campagneid)+';'

    #Recupération du fichier Excel a supprimer
    getExcel = 'SELECT Pathfile FROM campagne WHERE id = '+str(campagneid)+';'

    #Exécution de la requete et récupération du résultat
    con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()


    #Suppression des chemins de résolutions pour les sessions liées à la campagne. Les chemins sont stockés
    #dans les dossiers du repertoire Session portant le numéro de la campagne
    if os.path.exists(UPLOAD_FOLDER+'/Session/'+str(campagneid)):
        shutil.rmtree(UPLOAD_FOLDER+'/Session/'+str(campagneid))

    #Suppression des fichiers et dossiers liés aux campagnes
    cur.execute(getExcel)
    os.remove(cur.fetchone()[0])

    #Suppression du stockage des images et du fichier Drawning1.xml, si il y a des images
    if os.path.exists('static/img/Campagne_'+str(campagneid)):
        shutil.rmtree('static/img/Campagne_'+str(campagneid))


    #Supression de la campagne et des sessions de la base de donnée
    cur.execute(removeSession)
    cur.execute(removeCampagne)

    #Enregistrement des changements dans la base de donnée
    con.commit()

    #Fermeture de la base de donnée  
    con.close()

    #Rechargement de la page
    return campagne()

# =================================== Affichage des sessions =================================================
# ============================================================================================================

@app.route('/Banque', methods=["GET", "POST"])
def banque():

    # Construction des requetes : Recupération des campagnes et des sessions
    requestCampagne = "SELECT DISTINCT * FROM campagne;"
    requestSession = "SELECT DISTINCT * FROM session;"

    # Exécution de la requete et récupération des résultats
    # On souhaite afficher toutes les campagnes
    con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Execution des requetes
    cur.execute(requestCampagne)
    rowsCampagne = cur.fetchall(); 

    cur.execute(requestSession)
    rowsSession = cur.fetchall();


    con.close()

    return render_template("Banque.html", rowsCampagne = rowsCampagne, rowsSession = rowsSession)

# =================================== Affichage du chemin de la session ======================================
# ============================================================================================================

@app.route('/Chemin/<int:campagneid>/<int:sessionid>/', methods=["GET", "POST"])
def chemin(sessionid,campagneid):
    try : 

        #Recuperation information de la session
        requestSession = 'SELECT chemin FROM session WHERE sessionid = '+str(sessionid)+';'

        #Exécution de la requete et récupération du résultat
        con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(requestSession)

        #Récupération du chemin d'accés vers le fichier Excel
        chemin = cur.fetchone()[0]

        #Fermeture de la base de donnée  
        con.close()

        rows = jsonParsing(chemin)

        #La fonction buildIndic récupere le tableau des données, et construit des indicateurs avec.
        indics = buildIndic(rows)

        return render_template("Chemin.html",rows = rows, indics = indics, sessionid = sessionid,campagneid = campagneid)  

    except IOError : 

        print "Error 404 : file not found"
        pass

# =================================== Téléchargement du chemin format Excel ==================================
# ============================================================================================================

@app.route('/download/<int:campagneid>/<int:sessionid>/', methods=["GET", "POST"])
def download(campagneid,sessionid):
    #Recuperation information de la session
    requestSession = 'SELECT chemin FROM session WHERE sessionid = '+str(sessionid)+';'

    #Exécution de la requete et récupération du résultat
    con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(requestSession)

    #Récupération du chemin d'accés vers le fichier Excel
    chemin = cur.fetchone()[0]

    #Le tableau[-1] signifie que l'on prendra toujours le dernier tableau créé
    rows = jsonParsing(chemin)

    #La fonction buildIndic récupere le tableau des données, et construit des indicateurs avec.
    indics = buildIndic(rows)

    #Création du path du fichier excel de chemin stocké
    excelPath = UPLOAD_FOLDER+'/Session/'+str(campagneid)+'/'+binascii.hexlify(os.urandom(16))+'.xlsx'

    with open(excelPath,'w') as outfile:
        jsonToExcel(rows,indics,campagneid,excelPath)

    return send_file(excelPath,"Chemin_"+str(sessionid),as_attachment=True)


# =================================== Téléchargement de tous les participants à une campagne =================
# ============================================================================================================

@app.route('/downloadUser/<int:campagneid>', methods=["GET", "POST"])
def downloadUser(campagneid):
    #Recuperation information de la session
    requestSession = 'SELECT chemin FROM session WHERE campagneid = '+str(campagneid)+';'

    #Exécution de la requete et récupération du résultat
    con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(requestSession)

    #Le tableau[-1] signifie que l'on prendra toujours le dernier tableau créé
    rows = [jsonParsing(user[0]) for user in cur.fetchall()]

    #La fonction buildIndic récupere le tableau des données, et construit des indicateurs avec.
    indics = [buildIndic(indic) for indic in rows]

    #Création du path du fichier excel de chemin stocké
    excelPath = UPLOAD_FOLDER+'/Session/'+str(campagneid)+'/'+"Campagne_"+str(campagneid)+'.xlsx'

    with open(excelPath,'w') as outfile:
        jsonToExcelAll(rows,indics,campagneid,excelPath)

    return send_file(excelPath,"Campagne_"+str(campagneid),as_attachment=True)


# =================================== Envoit invitation ======================================================
# ============================================================================================================

@app.route('/Invits', methods=["GET", "POST"])
def invits():
    return render_template("Invits.html")

# =================================== Creation de campagne ===================================================
# ============================================================================================================

# Onglet de creation de campagnes : Upload de fichiers CSV
@app.route('/CreationDeCampagne', methods=['GET', 'POST'])
def upload_file():
    create_sql = ('CREATE TABLE IF NOT EXISTS campagne (  id INTEGER PRIMARY KEY,  nom varchar(20),  Pathfile varchar(20),  countdown int )')

    form = RegistrationForm(request.form) 
    if request.method == 'POST':

    # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        #Si tout se passe bien : Alors on upload le fichier, et on peuple la base de donnée
        if file and allowed_file(file.filename):

            #Le nom du fichier est identifiant aleatoire
            filename = binascii.hexlify(os.urandom(16))
            
            #Si les repertoires n'existent pas alors il sont créés
            if not os.path.exists(UPLOAD_FOLDER+"/ExcelFile"):
                os.makedirs(UPLOAD_FOLDER+"/ExcelFile")
        
            file.save(os.path.join(UPLOAD_FOLDER+"/ExcelFile", filename))

            # Peuplement de la base de donnée avec les données saisies par l'utilisateur
            con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
            
            # Requete d'insertion dans la base de donnée : Un nom et un chemin relatif
            # Vers le fichier CSV attaché à la campagne
            cur = con.cursor()

            #Creation de la table
            cur.execute(create_sql)

            requestInsert = 'INSERT INTO campagne (nom, Pathfile,countdown) VALUES (\"'+form.nom.data+'\",\"'+os.path.join(UPLOAD_FOLDER+"/ExcelFile", filename)+'\",'+form.countdown.data+');'
            print "Execution de la requête : " + requestInsert
            cur.execute(requestInsert)

            #Enregistrement des changements dans la base de donnée
            con.commit()
            con.close()
            

    return render_template("CreationDeCampagne.html", form=form)

# =================================== Scripts javascript =====================================================
# ============================================================================================================

# Route des fichiers Javascript
@app.route('/static/js/<filename>', methods=["GET", "POST"])
def answer_js(filename) :
    try : 
        return open(str(JS_PATH + filename)).read() 
    except IOError : 
        print "Error 404 : file not found"
        pass

# =================================== Traitement envoit JSON =================================================
# ============================================================================================================

# Recuperation du JSON envoyé par la completion d'une session par un répondant
# Traitement des données et alimentation de la table Session de la base de données
@app.route('/json_submit', methods=["GET","POST"])
def submit_handler():

    create_sql = ('CREATE TABLE IF NOT EXISTS session (  sessionid INTEGER PRIMARY KEY,  chemin TEXT,  campagneid INTEGER )')

    #Le fichier JSON du chemin est reçu depuis la page de la session, via une reqete AJAX
    file = request.get_json('json_submit')

    #Le chemin est enregistré dans un fichier temporaire afin de pouvoir le convertir en utf-8
    #Mais je ne suis pas convaincu de ce choix, je ne pense pas que cette étape est necessaire
    with open(app.config['UPLOAD_FOLDER']+'/data.json', 'w') as outfile:
        json.dump(file, outfile, ensure_ascii=False, encoding='utf8')

    #Le fichier JSON est enregistré dans un dictionnaire python
    dict_json = jsonParsing(app.config['UPLOAD_FOLDER']+'/data.json')

    #Exécution de la requete et récupération du résultat
    con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    #Creation de la table
    cur.execute(create_sql)

    #Le numéro de la campagne est retrouvé par une regex sur le nom de la session :
    #De la forme pa exemple : Session/1/ : On ne recherche que les digits ici
    campagneid = re.search(r'\d+', dict_json['SessionName']).group()

    #On récupere l'id de la derniere session ayant été effectuée dans la meme campagne
    lastrowid = cur.execute('SELECT count(sessionid) FROM session WHERE campagneid == '+campagneid+';').fetchone()[0]

    #Si c'est la premiere session jamais enregistrée, alors on évite que lastrowid = None
    if lastrowid == None:
        lastrowid = 0

    #Si les repertoires n'existent pas alors il sont créés
    if not os.path.exists(UPLOAD_FOLDER+dict_json['SessionName']):
        os.makedirs(UPLOAD_FOLDER+dict_json['SessionName'])

    #Insertion du tableau lié à la session dans la base de données
    json_path = UPLOAD_FOLDER+dict_json['SessionName']+'dataChemin'+str(int(lastrowid)+1)+'.json'
    insertTableau = 'INSERT INTO session (chemin, campagneId) VALUES (\"'+json_path+'\",'+str(campagneid)+');'

    #Le fichier json enegistrant le chemin de l'utilisateur dans sa session est enregistré
    with open(json_path,'w') as outfile:
        json.dump(file, outfile, ensure_ascii=False, encoding='utf8')


    #La base de donnée est alimentée et sauvegardée
    cur.execute(insertTableau)
    con.commit()
    con.close()


    return render_template("main.html")



# CLASSES
class RegistrationForm(Form):
    nom = StringField('Nom', [validators.Length(min=4, max=25)])
    countdown = StringField('countdown')
    
# MAIN 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
