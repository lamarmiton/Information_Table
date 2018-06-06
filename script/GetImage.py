#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile
import re

PATH_IMAGE = "static/img/Campagne_"


# ================================================== CLASSE IMAGE ===========================================================================

# La classe image est constitué d'un couple de coordonné ainsi que d'un path vers celle-ci.
# Les images sont stockés dans le fichier ../data/Upload/Campagne_{id_campagne}/medias

class Image:

	def __init__(self,noColonne, noLigne, imagePath):
		self.c = noColonne
		self.l = noLigne
		
		# On renseigne le path à partir du fichier static
		self.path = imagePath[7::]

# ======================================================= FIN CLASSE ========================================================================

# |==========================================================================================================================================|
# |   Cette fonction va chercher dans un fichier excel les fichiers necessaires à l'indexation des images de la façon suivante : 			 |
# |   Image : Numéro de la collone, Numéro de la ligne et le path vers celle-ci																 |
# |																																		     |
# | Explication : 																															 |
# |    																																		 |
# | Un fichier Excel est avant tout une archive. Tout comme une archive zip, nous pouvons y extraire les fichiers necessaires à la           |
# | construction du classeur xlsx. Ici, seulements deux choses nous interesses : Le repertoire média qui contient les images et les          |
# | vidéos affichés dans le classeur, ainsi que le fichier drawning1.xml. Le fichier xml est là pour indexer ces meme fichiers médias.       |
# | Il contiendra ainsi le numéro de collonne et de ligne de l'image en question. Nous le lierons avec la classe TableIb, pour y placer      |
# | les images dans la table.                                    																			 |
# | Une chose importante à savoir : Les images sont triées dans leurs ordres d'apparitions !												 |
# | Exemple : J'insere une image ancrée à la cellule 3 B, puis une image dans la cellule 2 A. les images seront respectivement nommée        |
# | image1 et image2.                          																								 |
# | 				                                                                                                                         |
# |	Fonctionnement et objectif de la fonction : 																						     |
# | 																																		 |
# | La fonction réalise les opérations suivantes : Extraction de "l'archive" xlxs. Creation de la liste des images au format jpg ou jpeg     |
# | récupération du fichier xml. Les fichiers sont stockés dans le serveur dans le dossier campagne + l'id de la campagne.					 |
# | Les coordonnées des collonnes des images dans leurs ordres d'appartion dans le fichier drawning1.xml. Les coordonnées des lignes.        |
# | Création des classes images en faisant coincider l'ordre d'apparition des coordonnées avec les noms des images.                          |
# | (Paire de coordonné 1 ==> Image1, Paire de coordonné 2 ==> Image 2, dans les deux cas, coordonné et nom des images correspond à leurs    |
# | ordres d'apparitions dans le classeur.																									 |
# |                                                                                                                                          |
# ============================================================================================================================================


def imageDansExcel(xlsxFile, idCampagne):
	Archive = zipfile.ZipFile(xlsxFile)
	ImageFiles = sorted([Archive.extract(F,PATH_IMAGE+str(idCampagne)) for F in Archive.namelist() if F.count('.jpg') or F.count('.jpeg')])
	DrawingXML = [Archive.extract(xml,PATH_IMAGE+str(idCampagne)) for xml in Archive.namelist() if xml.count('drawings/drawing1.xml')][0]

	# Application de la regex, nous souhaitons récuperer les valeurs dans les balises <xdr:col> et <xdr:row>
	coordCol = [re.compile("(?<=<xdr:col>).*?(?=<\/xdr:col>)").findall(elem) for elem in open(DrawingXML) if elem != None ][1]
	coordLig = [re.compile("(?<=<xdr:row>).*?(?=<\/xdr:row>)").findall(elem) for elem in open(DrawingXML) if elem != None ][1]

	# Retour de la liste des images
	return [Image(coordCol[i*2],coordLig[i*2],ImageFiles[i]) for i in range(len(ImageFiles))]

#======================================================= TEST ==================================================================================

#imageDansExcel("CSVExemples/ExempleExcel-copie.xlsx",2)