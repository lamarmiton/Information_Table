# -*- coding: utf-8 -*-
import statistics
import pandas as pd
import json

# FONCTION 

#Enleve les caractere nuisibles des tableaux transformés en chaine de caractere
def formatStr(string):
	return string.replace("]", "").replace("[","").replace("'","").replace("u","")

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


# Récupération des informations des chemins de TOUS LES PARTICIPANTS. Ecriture d'un fichier Excel à télécharger vers le client.
def jsonToExcelAll(rows,indics,campagneid,excelPath):

	writer = pd.ExcelWriter(excelPath)

	for user in range(len(rows)):

		pd.DataFrame({'Coords' : formatStr(str([ rows[user]['Chemin'][i]['Coords'] for i in range(len(rows[user]['Chemin'])) ])).encode("utf-8")},index = range(len(rows))).to_excel(writer,'Sheet1',index = None,header=None,startrow=user,startcol=1)
		pd.DataFrame({'Association Ligne' : formatStr(str([ rows[user]['Chemin'][i]['AssLig'] for i in range(len(rows[user]['Chemin'])) ])).encode("utf-8") },index = range(len(rows))).to_excel(writer,'Sheet1',index = None,header=None,startrow=user,startcol=2)
		pd.DataFrame({'Association Col' : formatStr(str([ rows[user]['Chemin'][i]['AssCol'] for i in range(len(rows[user]['Chemin'])) ])).encode("utf-8") },index = range(len(rows))).to_excel(writer,'Sheet1',index = None,header=None,startrow=user,startcol=3)
		pd.DataFrame({'Moyenne': indics[user]["Moyenne"], 'Temps total': indics[user]["Somme"],'Choix Final':rows[user]["FinalChoice"]},index = ['#']).to_excel(writer, sheet_name='Sheet1',index = None,header=None,startrow=user,startcol=4)
		#pd.DataFrame({'Choix Final': rows["FinalChoice"], 'Id Campagne': campagneid },index = ['#']).to_excel(writer,'Sheet1',startrow=len(rows['Chemin'])+2)

	writer.save()





# ==== Test =====

#jsonToExcel('../data/Upload/Session/3/dataChemin2.json')