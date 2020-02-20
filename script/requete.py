# -*- coding: utf-8 -*-

'''

Copyright 2018 RICHARD JEREMY

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. 
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, 
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import sqlite3

#SCRIPT DE REQUETAGE : Liaison avec la base de donnée

#Variable globale
DB_PATH = "data/"

def executeRequest(request):
    #Exécution de la requete et récupération du résultat
    con = sqlite3.connect(str(DB_PATH + "DbLigth.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(request)

    return cur,con


def init():
    cur,con = executeRequest('CREATE TABLE IF NOT EXISTS campagne (  id INTEGER PRIMARY KEY,  nom varchar(20),  Pathfile varchar(20),  countdown int, form1 TEXT, form2 TEXT )')
    cur,con = executeRequest('CREATE TABLE IF NOT EXISTS Chemin (  cheminid INTEGER PRIMARY KEY,  chemin TEXT,  campagneid INTEGER , token TEXT)')
    cur,con = executeRequest('CREATE TABLE IF NOT EXISTS Session (  id INTEGER PRIMARY KEY, token TEXT, campagneid INTEGER )')

    #Base de donnée des utilisateurs : Seulement un compte implenté pour question de sécuritée
    cur,con = executeRequest('CREATE TABLE IF NOT EXISTS Admin (  id INTEGER PRIMARY KEY, login TEXT, password INTEGER )')

    closeDB(con)


#Selection de toutes les campagnes dans la base de donnée
def selectAll(table):

    # Construction de la requête
    request = 'SELECT DISTINCT * FROM '+table+';'

    #Execution de la requete
    cur,con = executeRequest(request)
    return cur

#Selection d'un attribut dans une campagne
def selectFromTable(attr,table,select = ""):

    #Récupération du chemin d'accés vers le fichier Excel de la campagne
    request = 'SELECT '+attr+' FROM '+table

    if select != "":
    	request += ' WHERE '+select

    #Retour de la requete
    cur,con = executeRequest(request+';')
    return cur

#Supprime les éléments d'une table
def deleteFromTable(table,attr=""):
    
    #==== Construction de la requete =====

    #Ecriture des requetes de supression
    remove = 'DELETE FROM '+table

    #Si il y a des arguments 
    if attr != "":
        remove +=' WHERE '+attr

    cur,con = executeRequest(remove+";")
    closeDB(con)



#Insertion dans la table Campagne
def insertIntoCampagne(nom="",Pathfile="",countdown="",form1="",form2=""):

    requestInsert = 'INSERT INTO campagne (nom, Pathfile,countdown,form1,form2) VALUES (\"'+nom+'\",\"'+Pathfile+'\",\"'+countdown+'\",\"'+form1+'\",\"'+form2+'\");'
    cur,con = executeRequest(requestInsert)
    closeDB(con)


#Insertion dans la table Chemin
def insertIntoChemin(chemin="",campagneid="",token=""):

    requestInsert = 'INSERT INTO Chemin (chemin,campagneid,token) VALUES (\"'+chemin+'\",\"'+campagneid+'\",\"'+token+'\");'
    cur,con = executeRequest(requestInsert)
    closeDB(con)

#Insertion dans la table Session
def insertIntoSession(token="",campagneid=""):

    requestInsert = 'INSERT INTO Session (token,campagneid) VALUES (\"'+token+'\",\"'+str(campagneid)+'\");'
    cur,con = executeRequest(requestInsert)
    closeDB(con)
    


def closeDB(con):
    con.commit()
    con.close()
