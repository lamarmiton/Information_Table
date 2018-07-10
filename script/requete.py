# -*- coding: utf-8 -*-
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
    cur,con = executeRequest('CREATE TABLE IF NOT EXISTS campagne (  id INTEGER PRIMARY KEY,  nom varchar(20),  Pathfile varchar(20),  countdown int )')
    cur,con = executeRequest('CREATE TABLE IF NOT EXISTS Chemin (  cheminid INTEGER PRIMARY KEY,  chemin TEXT,  campagneid INTEGER , SessionName TEXT)')
    cur,con = executeRequest('CREATE TABLE IF NOT EXISTS Session (  id INTEGER PRIMARY KEY,  SessionName TEXT,  campagneid INTEGER )')
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
def insertIntoCampagne(nom="",Pathfile="",countdown=""):

    requestInsert = 'INSERT INTO campagne (nom, Pathfile,countdown) VALUES (\"'+nom+'\",\"'+Pathfile+'\",'+countdown+');'
    cur,con = executeRequest(requestInsert)
    closeDB(con)


#Insertion dans la table Chemin
def insertIntoChemin(chemin="",campagneid="",SessionName=""):

    requestInsert = 'INSERT INTO Chemin (chemin,campagneid,SessionName) VALUES (\"'+chemin+'\",\"'+campagneid+'\",\"'+SessionName+'\");'
    cur,con = executeRequest(requestInsert)
    closeDB(con)

#Insertion dans la table Session
def insertIntoSession(SessionName="",campagneid=""):

    requestInsert = 'INSERT INTO Session (SessionName,campagneid) VALUES (\"'+SessionName+'\",\"'+campagneid+'\");'
    cur,con = executeRequest(requestInsert)
    closeDB(con)
    


def closeDB(con):
    con.commit()
    con.close()
