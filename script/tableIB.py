#!/usr/bin/env python

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

# -*- coding: utf-8 -*-

from pandas import ExcelFile
import random
from collections import OrderedDict

#Importation des scripts adjacents
import case
import GetImage
############# DEFINITION DE LA CLASSE TABLE (Information Board)################################################################################################



#La classe Table est la classe principal. Elle va concevoir sur commande des tables d'informations aléatoire
#Grace à un fichier excel. Elle prend en argument la liste des tete de colonne (Produit ou critere) et la liste des lignes (produit ou colonne), pas les cases
#Elle mettra en relation les couples colonnes/lignes  avec l'objet case, afin de construire un tableau
#La classe Table est le coeur de la campagne


class Table:


	cases = []
	tableau = []

	def __init__(self,colonne, ligne, xlsfile, ImageTable):

		self.c = colonne
		self.l = ligne
		self.xls = xlsfile
		self.img = ImageTable
		self.createCase()
		self.createTableau()

	#Creation et alimentation de la liste de case de la table

	def createCase(self):

		#Creation d'une liste des valeurs du tableau
		values = []
		#Itérateur de cette meme liste
		ivalue = 0

		# On décompile les valeurs du fichier excel dans une liste
		[[values.append(row[1][i]) for row in self.xls.iterrows()] for i in range(len(self.c))]

		# Pour chaque colonnes : On créé un objet case composé d'un article et d'un critére
		for c in range(len(self.c)):
			for l in range (len(self.l)):

				self.cases.append(case.Case(self.c[c],self.l[l]).addValue(values[ivalue]))
				ivalue+=1

				# Si le classeur contient des images : Alors on lance la fonction addImage sur la derniere case ajoutée
				if self.img != []:
					self.addImage(self.cases[-1],c,l)

		
	#Fonction de creation de tableau  ordonné: Prend les colones, les lignes, et cherche les cases correspondantes
	#Un tableau est un dictionnaire ayant la syntaxe suivante : 
	#	==> { colonne [Critere 1, Critere 2], Ligne [Produit 1, Produit 2 ], Produit 1 [case, case], Produit 2 [case, case] }

	def createTableau(self):

		dictionnaire = OrderedDict()
		dictionnaire["colonne"] = random.sample([c for c in self.c],len(self.c))	
		dictionnaire["ligne"] = random.sample([l for l in self.l],len(self.l))

		for ligne in dictionnaire["ligne"]:
			dictionnaire[ligne] = [self.getCase(c,ligne).value for c in dictionnaire["colonne"]]

		# Si des images sont présentes dans le classeur Excel, Alors on lance la fonction addImage

		self.tableau.append(Tableau(dictionnaire))


	# La fonction addImage va vérifier si une image devrait se trouver à l'emplacement de la case.
	# Nous enlevons 1 à la valeur image.c et image.l (coordonné donné par la classe image), car la premiere cellule
	# en haut à droite est null et n'est pas prise en compte par le parsing de panda, on enleve donc cette case de difference

	def addImage(self,case,colonne,ligne):
		[case.addValue(image.path) for image in self.img if ( int(image.c)-1 == colonne and int(image.l)-1 == ligne )]

	#Récupere la valeur d'une case grace à sa colonne et à sa ligne
	def getCase(self,colonne,ligne):
		return [case for case in self.cases if ( case.c == colonne and case.l == ligne )][0]

########################## END ##################################################################################################################################


############################### DEFINITION DE LA CLASSE TABLEAU #################################################################################################

# La classe tableau, c'est le tableau affiché dans la session. Il affichera la table d'information suivant le fichier Excel
# Passé en argument dans la classe Table. La classe Table contient une liste des tableaux créés pour les retrouver.


class Tableau:

	def __init__(self,dictionnaire):

		self.dic = dictionnaire


########################## END ##################################################################################################################################

#Fonction de parsage de fichier excel avec pandas. Cette fonction appel toutes les autres. 
#La fonction parseExcel prend un fichier excel, et construi la table.


def parseExcel(xlsfile, idcampagne):

	# Dictionnaire des criteres ( prix, qualitée etc ... )
	# Dictionnaire des alternatives (Produit1 Produit2 Produit3)
	df = ExcelFile(xlsfile).parse(ExcelFile(xlsfile).sheet_names[0])
	alternatives = [row[0] for row in df.iterrows()]

	#Nous faisons venir la fonction Getimage.imageDansExcel qui nous renvois un tableau d'Image.
	#Celles-ci seront placés dans le tableau. En effet, Pandas ne récupere pas les images dans un classeur Excel :
	# Nous devons aller les chercher par nos propres moyens

	return Table(df.columns, alternatives,df,GetImage.imageDansExcel(xlsfile,idcampagne))
	


#### FIN FONCTION ###############################################################################################################################################		



##### TEST ######################################################################################################################################################

#Test des fonctions et classes de creation de tableau avec un fichier Excel quelquonque :

#parseExcel('CSVExemples/ExempleExcel-copie.xlsx',66)