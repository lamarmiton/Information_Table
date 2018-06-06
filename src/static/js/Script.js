/*							 VARIABLES GLOBALES									*/
/*		===================================================================		*/

var VALUES = [];
var COMPTEUR = [];
var COORDONNE = [];

var STARTIME = new Date();
var GLOBALTIME = new Date();
var COUNTDOWN = TIMER - (new Date() - GLOBALTIME)/1000
var TIMER = Number(document.body.children[5].innerText)

/* 									FONCTION 									*/
/*		====================================================================    */


// fonction au clic : Cache la div et affiche les infos
// Effet de flou pour avoir une transition sympa
function showCase(elmnt) {

	elmnt.style.filter = 'blur(40px)';
   	elmnt.style.transition = 'all 0.5s ease-out';

   	
    setTimeout( function () { elmnt.style.display = "none" } , 200);

	setTimeout( function () { elmnt.parentElement.children[1].style.display ="block" } , 200);

	VALUES.push(elmnt.parentElement.children[1].firstElementChild.attributes.alt.nodeValue)
	
	console.log()

	
	// Récupération de l'association en ligne
	assLig = unescape(decodeURIComponent(elmnt.parentElement.parentElement.children[0].innerText));
		
	// Récupération de l'association en colonne
	// ==> Récupération de l'entete du tableau : On récupere la n eme case, ou n est le coordonné en colonne
	assCol = unescape(decodeURIComponent(elmnt.parentElement.offsetParent.children[0].childNodes[1].children[elmnt.parentElement.cellIndex].innerText));

	// Coordonné en colonne
	coordCol = elmnt.parentElement.cellIndex;
	// Coordonné en ligne
	coordLig = elmnt.parentElement.parentElement.rowIndex;

	// Construction de l'objet coordonnees
	var coordonnes = " [ "+assLig+" / "+assCol+" ] || [   Ligne : "+coordLig+" Colonne : "+coordCol+" ] "
	
	COORDONNE.push(coordonnes)
};

// Fonction de zoom sur une info révélée
function zoomIn (elmnt) {

 zoom.to({
    element: elmnt.children[0],
    padding: 75
  });

};

function ValideSession (elmnt) {

	chemin = { "FinalChoice" : unescape(decodeURIComponent(elmnt)), "SessionName" : window.location.pathname, "Chemin" : [] }
  	index = 0
	VALUES.forEach(function(value){

		var chainon = { "Nb": index+1, "Value" :value, "Compteur" : COMPTEUR[index], "Coords" : COORDONNE[index] }
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

	document.body.children[4].style.display="block"
	// Un retour immediat annule la requete, donc, on attends 200ms et c'est le retour à l'index
	setTimeout(function() {
		window.location = "/";
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
    console.log(" VALUES actuel :  "+ VALUES )
    console.log(" coordonnés actuels :  "+ COORDONNE )

	}, 500)

});


// Mets fin à l'experience, construction du fichier JSON à exporter
$(".alternative").click(function(){
  	ValideSession($(this)[0].innerText);
});

// Compte à rebours

/* Fonction de compte à rebours : 
	
	- document.body.children[5] est la div de compte à rebours
	- GLobaltime est la date d'ouverture de la session
	- Le temps est déterminé à la création de la campagne
	- Les 10 dernieres secondes ont pour but d'etre anxiogène
*/

var interval = setInterval(function() {

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


}, 1);




});