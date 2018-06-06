import pandas as pd
import json

# FONCTION 

#Parsing de fichier JSON
def jsonParsing(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)

    return data

#Transforme le fichier json D'UN CHEMIN en un fichier excel
def jsonToExcel(jsonPath,excelPath):
	df_json = pd.read_json(jsonPath, encoding = "utf-8").apply( lambda x: pd.Series([x[0]["Nb"],x[0]["Coords"],x[0]["Compteur"],x[0]["Value"]]), axis = 1 )
	df_json.columns = ['#','Coords','Compteur','Value']
	writer = pd.ExcelWriter(excelPath)
	df_json.to_excel(writer,'Sheet1',index=False)
	writer.save()





# ==== Test =====

#jsonToExcel("../data/Upload/Session/3/dataChemin2.json")