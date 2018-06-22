# -*- coding: utf-8 -*-
import statistics
import pandas as pd
import json

# FONCTION 

#Prend en entrée un dictionnaire Json, et construit des indicateurs avec
def buildIndic(rows):

	indicateurs = {}
	indicateurs['Moyenne'] = statistics.mean([row['Compteur'] for row in rows['Chemin']])
	indicateurs['Somme'] = sum([row['Compteur'] for row in rows['Chemin']])

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
	return excelPath





# ==== Test =====

#jsonToExcel('../data/Upload/Session/3/dataChemin2.json')