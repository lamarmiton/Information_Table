# -*- coding: utf-8 -*-

#Import FLASK
from flask import Flask, flash, request, redirect, url_for, render_template, send_file

#Import de login
from flask_simplelogin import SimpleLogin
from flask_simplelogin import is_logged_in
from flask_simplelogin import login_required

#Import formulaires
from werkzeug.utils import secure_filename
from wtforms import Form, FieldList, SelectField, StringField, PasswordField, validators

#Import divers
import re
import json
import os
import sys
import shutil
import binascii

#IMPORT DU REPERTOIRE DE SCRIPT PYTHON
sys.path.insert(1,'script/')
from tableIB import parseExcel
from jsonParsing import jsonParsing, jsonToExcel, buildIndic,jsonToExcelAll
import requete as req

import base64
#ENCODAGE UTF8
reload(sys)
sys.setdefaultencoding('utf-8')

# CHEMINS ABSOLUS 
VIEWS_PATH = "static/views/"
JS_PATH = "static/js/"
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
app.config['SECRET_KEY'] = 'something-secret'


#Pour le moment, et pour des raisons de test, il n'y a qu'un seul compte admin
app.config['SIMPLELOGIN_USERNAME'] = req.selectFromTable("login","Admin").fetchone()[0]
app.config['SIMPLELOGIN_PASSWORD'] = base64.b64decode(req.selectFromTable("password","Admin").fetchone()[0])





# =================================== Login ==================================================================
# ============================================================================================================

#Page de login de l'administrateur
@app.route('/login')
def login():
    return render_template("login.html")

# =================================== Index ==================================================================
# ============================================================================================================

# ROUTES    
@app.route('/')
@login_required
def index():
    return render_template("main.html")

# =================================== Affichage de toutes les campagnes ======================================
# ============================================================================================================

#Dans la page campagne, on affiche la liste des campagnes
@app.route('/Campagne', methods=["GET", "POST"])
@login_required
def campagne():

    if is_logged_in():
        rows = req.selectAll("campagne").fetchall()
        return render_template("Campagne.html", rows = rows)


    else:
        return redirect("/login", code=302)



# ======================================= Affichage détaillé des campagnes ===================================
# ============================================================================================================

#Affiche les differentes campagnes
@app.route('/Campagne/<int:campagneid>/', methods=["GET", "POST"])
@login_required
def detailCampagne(campagneid):

    #Récupération du chemin d'accés vers le fichier Excel
    chemin = req.selectFromTable("Pathfile","campagne","id ="+str(campagneid)).fetchone()[0]

    name = req.selectFromTable("nom","campagne","id ="+str(campagneid)).fetchone()[0]

    countdown = int(req.selectFromTable("countdown","campagne","id ="+str(campagneid)).fetchone()[0])

    #Construction du tableau grâce au script python tableIDB.python
    #Le tableau[-1] signifie que l'on prendra toujours le dernier tableau créé
    rows = parseExcel(str(chemin),campagneid).tableau[-1].dic

    return render_template("InformationBoard.html",rows = rows, name = name, countdown = countdown)  



# ===================================================== Gestion des sessions =================================
# ============================================================================================================

@app.route('/Session', methods=["GET", "POST"])
@login_required
def BanqueSession():

    if is_logged_in():
        #Selection des campagnes
        rowsCampagne = req.selectAll("campagne").fetchall()

        return render_template("BanqueSession.html", rowsCampagne = rowsCampagne)

    else:
        return redirect("/login", code=302)

# =================================== Session : Table d'information ==========================================
# ============================================================================================================

#Page de la session : La complétion de l'étude par un répondant
#La creation de la session est lié à la campagne (Retrouvée par son id)
#La session est généré aléatoirement via le fichier Excel de la campagne
@app.route('/Session/<int:campagneid>/<string:token>', methods=["GET", "POST"])
def session(campagneid,token):

    #Récupération du chemin d'accés vers le fichier Excel
    chemin = req.selectFromTable("Pathfile","campagne","id ="+str(campagneid)).fetchone()[0]

    name = req.selectFromTable("nom","campagne","id ="+str(campagneid)).fetchone()[0]

    countdown = int(req.selectFromTable("countdown","campagne","id ="+str(campagneid)).fetchone()[0])

    #Construction du tableau grâce au script python tableIDB.python
    #Le tableau[-1] signifie que l'on prendra toujours le dernier tableau créé
    rows = parseExcel(str(chemin),campagneid).tableau

    return render_template("Session.html",rows = rows[-1].dic, name = name, countdown = countdown,campagneid = campagneid, token = token)  


#Page de la session : La complétion de l'étude par un répondant
#La creation de la session est lié à la campagne (Retrouvée par son id)
#Le token de session est généré aléatoirement, et fait le lien entre la page 1 du formulaire, la table d"information
# Et la page 2 du formulaire Google
@app.route('/Form_1/<int:campagneid>/', methods=["GET", "POST"])
def form1(campagneid):
    token = "C"+str(campagneid)+"ID"+binascii.hexlify(os.urandom(3))
    req.insertIntoSession(token,campagneid)

    form1 = req.selectFromTable("form1","campagne","id = "+str(campagneid)).fetchone()[0]

    return render_template("Form_1.html",campagneid = campagneid, token = token, form1 = form1)  



#Page de la session : La complétion de l'étude par un répondant
#La creation de la session est lié à la campagne (Retrouvée par son id)
@app.route('/Form_2/<int:campagneid>/<string:token>', methods=["GET", "POST"])
def form2(campagneid,token):

    form2 = req.selectFromTable("form2","campagne","id = "+str(campagneid)).fetchone()[0]
    return render_template("Form_2.html",campagneid = campagneid, token = token, form2 = form2)  



# =================================== Submit ==================================================================
# ============================================================================================================

# ROUTES    
@app.route('/Submit', methods=["GET", "POST"])
def submit():
    return render_template("Submit.html")


# =================================== Remove Campagne ========================================================
# ============================================================================================================

#Supression de la campagne : Balayage et ménage des fichiers liés à celle-ci
@app.route('/Delete/<int:campagneid>/', methods=["DELETE","GET"])
@login_required
def delete(campagneid):

    #Suppression des chemins de résolutions pour les sessions liées à la campagne. Les chemins sont stockés
    #dans les dossiers du repertoire Session portant le numéro de la campagne
    if os.path.exists(UPLOAD_FOLDER+'/Campagne/'+str(campagneid)):
        shutil.rmtree(UPLOAD_FOLDER+'/Campagne/'+str(campagneid))

    #Suppression des fichiers et dossiers liés aux campagnes
    os.remove(req.selectFromTable("Pathfile","campagne","id ="+str(campagneid)).fetchone()[0])

    #Suppression du stockage des images et du fichier Drawning1.xml, si il y a des images
    if os.path.exists('static/img/Campagne_'+str(campagneid)):
        shutil.rmtree('static/img/Campagne_'+str(campagneid))


    #Supression de la campagne et des sessions de la base de donnée
    req.deleteFromTable("Chemin","campagneid = "+str(campagneid))
    #Supression de la session et des chemins de la base de donnée
    req.deleteFromTable("Session","campagneid = "+str(campagneid))
    #Supression de la campagne et des sessions de la base de donnée
    req.deleteFromTable("campagne","id = "+str(campagneid))

    #Rechargement de la page
    return campagne()

# =================================== Affichage des sessions =================================================
# ============================================================================================================

@app.route('/Chemin', methods=["GET", "POST"])
@login_required
def banque():
    if is_logged_in():
        #Selection des campagnes
        rowsCampagne = req.selectAll("campagne").fetchall()
        #Selection des chemin
        rowsChemin = req.selectAll("Chemin").fetchall()
        #Selection des sessions
        rowsSession = req.selectAll("Session").fetchall()

        return render_template("Banque.html", rowsCampagne = rowsCampagne, rowsChemin = rowsChemin, rowsSession = rowsSession)

    else:
        return redirect("/login", code=302)

# =================================== Affichage du chemin de la session ======================================
# ============================================================================================================

@app.route('/Chemin/<int:campagneid>/<int:cheminid>/', methods=["GET", "POST"])
@login_required
def chemin(cheminid,campagneid):

    #Selection du JSon d'un chemin
    rows = jsonParsing(str(req.selectFromTable("chemin","Chemin","cheminid ="+str(cheminid)).fetchone()[0]))

    #La fonction buildIndic récupere le tableau des données, et construit des indicateurs avec.
    indics = buildIndic(rows)

    token = req.selectFromTable("token","Chemin","cheminid ="+str(cheminid)).fetchone()[0]
    return render_template("Chemin.html",rows = rows, indics = indics, cheminid = cheminid,campagneid = campagneid, token = token)  


# =================================== Téléchargement du chemin format Excel ==================================
# ============================================================================================================

@app.route('/download/<int:campagneid>/<int:cheminid>/', methods=["GET", "POST"])
@login_required
def download(campagneid,cheminid):

    #Selection du JSon d'un chemin
    rows = jsonParsing(req.selectFromTable("chemin","Chemin","cheminid ="+str(cheminid)).fetchone()[0])

    #La fonction buildIndic récupere le tableau des données, et construit des indicateurs avec.
    indics = buildIndic(rows)

    #Création du path du fichier excel de chemin stocké
    excelPath = UPLOAD_FOLDER+'/Session/'+str(campagneid)+'/'+binascii.hexlify(os.urandom(16))+'.xlsx'

    with open(excelPath,'w') as outfile:
        jsonToExcel(rows,indics,campagneid,excelPath)

    return send_file(excelPath,"Chemin_"+str(cheminid),as_attachment=True)


# =================================== Téléchargement du fichier Excel de référence  ==========================
# ============================================================================================================

@app.route('/downloadExemple', methods=["GET", "POST"])
@login_required
def downloadExemple():
    return send_file("data/Exemple.xlsx",as_attachment=True)


# =================================== Téléchargement de tous les participants à une campagne =================
# ============================================================================================================

@app.route('/downloadUser/<int:campagneid>', methods=["GET", "POST"])
@login_required
def downloadUser(campagneid):

    #Le tableau[-1] signifie que l'on prendra toujours le dernier tableau créé
    rows = [jsonParsing(user[0]) for user in req.selectFromTable("chemin","Chemin","campagneid ="+str(campagneid)).fetchall()]

    #Liste des noms des participants à la campagne
    token = [user for user in req.selectFromTable("token","Chemin","campagneid ="+str(campagneid)).fetchall()]

    #La fonction buildIndic récupere le tableau des données, et construit des indicateurs avec.
    indics = [buildIndic(indic) for indic in rows]

    #Création du path du fichier excel de chemin stocké
    excelPath = UPLOAD_FOLDER+'/Session/'+str(campagneid)+'/'+"Campagne_"+str(campagneid)+'.xlsx'

    with open(excelPath,'w') as outfile:
        jsonToExcelAll(rows,indics,campagneid,excelPath,token)

    return send_file(excelPath,"Campagne_"+str(campagneid),as_attachment=True)


# =================================== Creation de campagne ===================================================
# ============================================================================================================

# Onglet de creation de campagnes : Upload de fichiers CSV
@app.route('/CreationDeCampagne', methods=['GET', 'POST'])
@login_required
def upload_file():

    if is_logged_in():

        form = FormCampagne(request.form) 
        if request.method == 'POST':

            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']

            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '' :
                flash('No selected file')
                return redirect(request.url)

            #Si tout se passe bien : Alors on upload le fichier, et on peuple la base de donnée
            if file and allowed_file(file.filename):


                if form.nom.data not in req.selectFromTable("nom","campagne").fetchall():

                    #Le nom du fichier est identifiant aleatoire
                    filename = binascii.hexlify(os.urandom(16))
                    
                    #Si les repertoires n'existent pas alors il sont créés
                    if not os.path.exists(UPLOAD_FOLDER+"/ExcelFile"):
                        os.makedirs(UPLOAD_FOLDER+"/ExcelFile")

                    req.insertIntoCampagne(form.nom.data,os.path.join(UPLOAD_FOLDER+"/ExcelFile", filename),form.countdown.data,form.form1.data,form.form2.data)
                    file.save(os.path.join(UPLOAD_FOLDER+"/ExcelFile", filename))

                    return redirect("/Campagne", code=302)

    else:
        return redirect("/login", code=302)

            

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

    #Le fichier JSON du chemin est reçu depuis la page de la session, via une reqete AJAX
    file = request.get_json('json_submit')

    #Le chemin est enregistré dans un fichier temporaire afin de pouvoir le convertir en utf-8
    #Mais je ne suis pas convaincu de ce choix, je ne pense pas que cette étape est necessaire
    with open(app.config['UPLOAD_FOLDER']+'/data.json', 'w') as outfile:
        json.dump(file, outfile, ensure_ascii=False, encoding='utf8')

    #Le fichier JSON est enregistré dans un dictionnaire python
    dict_json = jsonParsing(app.config['UPLOAD_FOLDER']+'/data.json')

    
    #Le numéro de la campagne est retrouvé par une regex sur le nom de la session :
    #De la forme pa exemple : Session/1/ : On ne recherche que les digits ici
    campagneid = re.search(r'\d+', dict_json['CampagneID']).group()

    #On récupere l'id de la derniere session ayant été effectuée dans la meme campagne ( qui correspond au nombre de chemin)
    lastrowid = len(req.selectAll("Chemin").fetchall())

    #Si c'est la premiere session jamais enregistrée, alors on évite que lastrowid = None
    if lastrowid == None:
        lastrowid = 0

    #Si les repertoires n'existent pas alors il sont créés  
    if not os.path.exists(UPLOAD_FOLDER+dict_json['CampagneID']):
        os.makedirs(UPLOAD_FOLDER+dict_json['CampagneID'])

    #Insertion du tableau lié à la session dans la base de données
    json_path = UPLOAD_FOLDER+dict_json['CampagneID']+'dataChemin'+str(int(lastrowid)+1)+'.json'
    print campagneid

    token = dict_json['Token']
    
    req.insertIntoChemin(json_path,str(campagneid),token)

    #Le fichier json enegistrant le chemin de l'utilisateur dans sa session est enregistré
    with open(json_path,'w') as outfile:
        json.dump(file, outfile, ensure_ascii=False, encoding='utf8')


    return render_template("main.html")



# CLASSES

#Formulaire de saisie

#Création de campagne
class FormCampagne(Form):
    nom = StringField('Nom de l\'expérience', [validators.Length(min=4, max=25)])
    countdown = StringField('Durée de l\'expérience')
    form1 = StringField('Formulaire 1')
    form2 = StringField('Formulaire 2')







# MAIN 
if __name__ == '__main__':
    
    
    SimpleLogin(app)

    #Initialisation de la base de donnée
    req.init()
    #Connexion de l'application au port 8080
    app.run(host='0.0.0.0', port=8080)
