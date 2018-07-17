# -*- coding: utf-8 -*-
import statistics
import pandas as pd
import json
import pprint as p
from collections import OrderedDict

# FONCTION 

#Enleve les caractere nuisibles des tableaux transformés en chaine de caractere
def formatStr(string):
    return string.replace("]", "").replace("[","").replace("u'","")

#Prend en entrée un dictionnaire Json, et construit des indicateurs avec
def buildIndic(rows):

    indicateurs = {}

    try:
        indicateurs['Moyenne'] = statistics.mean([row['Compteur'] for row in rows['Chemin']])
        indicateurs['Somme'] = sum([row['Compteur'] for row in rows['Chemin']])
    except: 
    	indicateurs['Moyenne'] = "Erreur dans la construction de l'indicateur"
        indicateurs['Somme'] = "Erreur dans la construction de l'indicateur"
        pass

    return indicateurs

#Parsing de fichier JSON
def jsonParsing(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)

    return data

# Récupération des informations du chemin et écriture d'un fichier Excel à télécharger vers le client
def jsonToExcel(rows,indics,campagneid,excelPath):

    writer = pd.ExcelWriter(excelPath)
    pd.DataFrame(rows['Chemin']).to_excel(writer,'Sheet1',index=False)
    pd.DataFrame({'Temps passé en moyenne ': indics["Moyenne"], 'Temps total': indics["Somme"]},index = ['#']).to_excel(writer, sheet_name='Sheet1',startcol=6)
    pd.DataFrame({'Choix Final': rows["FinalChoice"], 'Id Campagne': campagneid },index = ['#']).to_excel(writer,'Sheet1',startrow=len(rows['Chemin'])+2)
    writer.save()


# Récupération des informations des chemins de TOUS LES PARTICIPANTS. Ecriture d'un fichier Excel à télécharger vers le client.
def jsonToExcelAll(rows,indics,campagneid,excelPath,SessionNames):

    writer = pd.ExcelWriter(excelPath)

    #Id de la session 
    d = OrderedDict()
    d['Token'] = ''
    d['Coords'] = ''
    d['Association Ligne'] = ''
    d['Association Col'] = ''
    d['Moyenne'] = ''
    d['Temps total'] = ''
    d['Choix Final'] = ''
    d['Id Campagne'] = ''

    pd.DataFrame(d,index = range(8)).to_excel(writer,'Sheet1',index = None,startrow=0,startcol=0)
    
    for user in range(len(rows)):

        #Id de la session 
        pd.DataFrame({'Session' :  SessionNames[user] }).to_excel(writer,'Sheet1',index = None,header=None,startrow=user+1,startcol=0)
        
        #Chemin en coordonnée :
        pd.DataFrame({'Coords' : formatStr(str([ rows[user]['Chemin'][i]['Coords'] for i in range(len(rows[user]['Chemin'])) ])).encode("utf-8")},index = range(len(rows))).to_excel(writer,'Sheet1',index = None,header=None,startrow=user+1,startcol=1)
        
        #Association en Ligne :
        pd.DataFrame({'Association Ligne' : formatStr(str([ rows[user]['Chemin'][i]['AssLig'] for i in range(len(rows[user]['Chemin'])) ])).encode("utf-8") },index = range(len(rows))).to_excel(writer,'Sheet1',index = None,header=None,startrow=user+1,startcol=2)
        
        #Association en colonne :
        pd.DataFrame({'Association Col' : formatStr(str([ rows[user]['Chemin'][i]['AssCol'] for i in range(len(rows[user]['Chemin'])) ])).encode("utf-8") },index = range(len(rows))).to_excel(writer,'Sheet1',index = None,header=None,startrow=user+1,startcol=3)
        
        #Moyenne de temps passé et somme
        pd.DataFrame({'Moyenne': indics[user]["Moyenne"], 'Temps total': indics[user]["Somme"]},index = ['#']).to_excel(writer, sheet_name='Sheet1',index = None,header=None,startrow=user+1,startcol=4)
        
        #Choix Final du chemin
        pd.DataFrame({'Choix Final':rows[user]["FinalChoice"], 'Id Campagne': campagneid },index = range(len(rows))).to_excel(writer,'Sheet1',index = None,header=None,startrow=user+1,startcol=6)


    writer.save()




# ==== Test =====

#jsonToExcel('../data/Upload/Session/3/dataChemin2.json')