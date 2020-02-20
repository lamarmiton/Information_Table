/*

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

*/
/*							 VARIABLES GLOBALES									*/
/*		===================================================================		*/

var COMPTEUR = [];
var ASSLIG = [];
var ASSCOL = [];
var COORD =[ ];


var STARTIME = new Date();
var GLOBALTIME = new Date();
var COUNTDOWN = TIMER - (new Date() - GLOBALTIME)/1000
var TIMER = Number(document.body.children[5].innerText)

/* 									FONCTION 									*/
/*		====================================================================    */


// fonction au clic : Cache la div et affiche les infos
// Effet de flou pour avoir une transition sympa
function showCase(elmnt) {



	/*                 Affiche toutes les div servant à cacher l'information */
	var elements = document.getElementsByClassName("hideInfo")

    for (var i = 0; i < elements.length; i++){
        elements[i].style.display = "block";
        elements[i].style.filter = "none";

    }

    /*                  Cache les infos                     */
   	var elements = document.getElementsByClassName("info")

    for (var i = 0; i < elements.length; i++){
        elements[i].style.display = "none";

    }


	elmnt.style.filter = 'blur(40px)';
   	elmnt.style.transition = 'all 0.5s ease-out';

   	
    setTimeout( function () { elmnt.style.display = "none" } , 200);

	setTimeout( function () { elmnt.parentElement.children[1].style.display ="block" } , 200);

	
	// Récupération de l'association en ligne
	assLig = unescape(decodeURIComponent(elmnt.parentElement.parentElement.children[0].innerText));
		
	// Récupération de l'association en colonne
	// ==> Récupération de l'entete du tableau : On récupere la n eme case, ou n est le coordonné en colonne
	assCol = unescape(decodeURIComponent(elmnt.parentElement.offsetParent.children[0].childNodes[1].children[elmnt.parentElement.cellIndex].innerText));

	// Coordonné en colonne
	coordCol = elmnt.parentElement.cellIndex;
	// Coordonné en ligne
	coordLig = elmnt.parentElement.parentElement.rowIndex;
	
	ASSLIG.push(assLig)
	ASSCOL.push(assCol)
	COORD.push(coordCol+":"+coordLig)

	

};

// Fonction de zoom sur une info révélée
function zoomIn (elmnt) {

 zoom.to({
    element: elmnt.children[0],
    padding: 75
  });

};

function ValideSession (elmnt,location) {

	chemin = { "Token" : window.location.pathname.substring(11, window.location.pathname.length), "FinalChoice" : unescape(decodeURIComponent(elmnt)), "CampagneID" : window.location.pathname, "Chemin" : [] }
  	index = 0
	ASSLIG.forEach(function(value){

		var chainon = { "Nb": index+1, "Compteur" : COMPTEUR[index], "AssLig" : ASSLIG[index],"AssCol" : ASSCOL[index],"Coords" : COORD[index]}
		chemin.Chemin.push(chainon)
		++index	
	})
		
	// Post le chemin au format JSON
	var request = $.ajax({
	    url: "/json_submit",
	    type: "POST",
	    contentType: "application/json",
	    data: JSON.stringify(chemin),  
	    dataType: "json",
	  }).done( function () { 
	  	console.log("Json sent");
	})

	document.getElementsByClassName("loading")[0].style.display="block"
	// Un retour immediat annule la requete, donc, on attends 200ms et c'est le retour à l'index
	setTimeout(function() {
		window.location = location ;
	},2000)
};


/*								DEBUT DE SESSION 									*/
/*		====================================================================		*/


$(document).ready(function () {

// Au clic sur un point d'interrogation
$(".hideInfo").click(function(){

	// Ajout du temp au tableau de compteur
	COMPTEUR.push(new Date() - STARTIME)
	// Reset du compteur
    STARTIME = new Date();

	setTimeout(function () {

    console.log(" Liste des compteurs :  "+ COMPTEUR )
    console.log(" Coordonnés actuels :  "+COORD)
    console.log(" Association colonne :  "+ASSCOL)
    console.log(" Association ligne :  "+ASSLIG)

	}, 500)


});


// Compte à rebours

/* Fonction de compte à rebours : 
	
	- document.body.children[5] est la div de compte à rebours
	- GLobaltime est la date d'ouverture de la session
	- Le temps est déterminé à la création de la campagne
	- Les 10 dernieres secondes ont pour but d'etre anxiogène
	- Temps infini lorsque l'administrateur tape 00
*/

var interval = setInterval(function() {

	if ( document.body.children[5].innerText != "00") {

		if ( COUNTDOWN != 0 ) {

		    if (Math.round(COUNTDOWN) < 10){
		    	COUNTDOWN = (TIMER - (new Date() - GLOBALTIME)/1000).toFixed(2);
		    	document.body.children[5].innerText = COUNTDOWN;
		    	document.body.children[5].style.color="red";
		    	document.body.children[5].style.fontSize = "25px";
		    }

			else{
				COUNTDOWN = Math.round(TIMER - (new Date() - GLOBALTIME)/1000);
		    	document.body.children[5].innerText = COUNTDOWN
		    	document.body.children[5].style.fontSize = "20px";
		    }

		}

	    if ( COUNTDOWN ==  0.10 ){
	    	COUNTDOWN = 0
	    	document.body.children[5].innerText = 0
			ValideSession("Time out !");

		}
	}

}, 1);
	
});