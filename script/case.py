#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################## DEFINITION DE LA CLASSE CASE ########################################################################################################


# La case est la combinaison d'un critere (En collonne ou ligne peu importe)
# Et d'une valeur. Cela permet de retrouver chaque case lorsqu'elles seront mélangées

class Case:
    value = None

    def __init__(self, collonne, ligne):
        self.c = collonne
        self.l = ligne

    def addValue(self,value):
        self.value = value
        return self

########################## END ##################################################################################################################################
