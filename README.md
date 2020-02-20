<!-- 
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
-->


<div class="container">


<h1 class="titre"> Index : Creation de table d'informations </h1>

<h2 class="titre"> Manuel d'utilisation </h2>

<h3 class="titre">Introduction</h3>
<p>Bonjour, et bienvenue dans l'application de création de table d'information.

L'application fonctionne autour des créations de campagne. Une campagne est un modèle à partir duquel une session
est générée. Vous pourrez récupérer le chemin de résolution du participant dans la banque de données.</p>


<h3 class="titre">Les campagnes</h3>

<p> 
Pour créer une campagne, rendez vous dans l'onglet création de campagne. Vous devrez renseigner le nom de la campagne,
la durée de la campagne en seconde, ainsi qu'un fichier Excel au format <b>.xlsx</b>. Le fichier devra être de la forme suivante :
</p>

<a href="https://docs.google.com/spreadsheets/d/1lutLO8j5i3Ne5qgTy-vfPjOte-Y8iAMST4P5cjwYgQo/edit#gid=0" > <img src="https://i.imgur.com/GJJIXM4.png"> </a>

<p>
  La première case du tableau, en haut à droite dois être vide. Les critères (en rouge) sont en haut du tableau uniquement.Les produits (en bleu), c'est-à-dire le choix que devra faire le participant se trouve dans la première colonne du tableau. Les cases (en jaune) forment le reste du tableau et forment une association entre un critère et un produit.
</p>

<h3 class="titre">Les sessions</h3>

<p>
Les sessions sont générées aléatoirement à partir d'une campagne. Les produits et les criteres seront placés aléatoirement pour creer le tableau. Les cases étant des
associations, la session est construite sur ce principe. Vous pourrez participer à une session en allant dans l'onglet "participer à une session". Pour le moment,
l'inviation à une session n'est pas disponible. Vous pourrez toutefois copier le lien de la session. Le numéro de la session figure au bout du lien. le participant
recevant la session pourra alors compléter celle-ci.
</p>

<h3 class="titre">Les chemins de réalisation</h3>

<p>
Les chemins de résolutions sont disponibles dans l'onglet banque de données. Vous pourrez retrouver les sessions par leurs numéros, elles sont triées par campagne.
</p>


<h3 class="titre">Invitation à une session</h3>

<p> 
Pour inviter un participant à une session, cliquez sur l'onglet " Invitation à une session ". Saississez un identifiant ( son nom, prenom, numéro, pseudo etc .. ) et liez le à une campagne.
Vous retrouverez le participant dans l'onglet " Banque de session ". L'identifiant appraitra, ainsi qu'un lien vers sa session. Vous pourrez ainsi envoyer ce lien à votre guise vers l'individu.
</p>



<h3 class="titre"> Première connexion au logiciel et environnement de travail </h3>

<p> 
Pour se connecter au logiciel, par défaut, le nom de compte et le mot de passe :

__nom de compte__ : admin

__mot de passe__ : tableinfo

Le logiciel utilise python 2
</p>

</div>
</body>

</html>
