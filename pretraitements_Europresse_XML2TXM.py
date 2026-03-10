'''
Prétraitements pour passer d'un corpus XML/XTZ récupéré depuis Europresse avec le Press Corpus Scraper (Moncomble). 
Plusieurs fonctionnalités peuvent être appliquées à un répertoire qui contient les fichiers XML : 
- Nettoyage : il y a parfois des balises <b> et </b> dans l'attribut title de l'élément text (vu avec Sud_Ouest_auteurinconnu)
- Ajouter un attribut : pour faire un corpus partitionné selon des critères autres que ceux qui sont présents en attribut de text (source, author, title, date), on peut récolter des sous-corpus et y ajouter l'attribut qui correspond (ex : couverture, tonalité, pays, langue, etc.).
- Date : la date est au format aaaa/mm/dd, on peut aussi ajouter un attribut annee (yyyy) et un attribut mois (yyyy-mm) pour les corpus dont la couverture temporelle est étendue. 

03/2026
Marine Delaborde
'''

from pathlib import Path
import re

# Chemin vers le répertoire qui contient les fichiers XML
#repertoire_xml = Path("/chemin/vers/rep_XML")

# Fonctionnalités du script : oui ou non ?
ajouter_attribut = True # ou False
nettoyer_titre = True # ou False
changer_date = True # ou False | Cela revient à ajouter deux attibuts : mois et annee

# Liste d'attributs à ajouter à la fin de l'élément text : ajouter autant de lignes que d'attributs souhaités
new_attributs = {
	"couverture":"nationale", 
	"langue":"fra"
}

# Patrons regex
patron_text = re.compile(r'(<text\b[^>]*?)>') # Toute la balise text
patron_title = re.compile(r'title="([^"\n]*)"') # Juste l'attribut title
patron_balises = re.compile(r'</?[bi]>') # Balises à supprimer <b>, </b>, <i> et </i>
patron_date = re.compile(r'date="(\d{4})-(\d{2})-(\d{2})"') # Date de publication

def clean_title(match):
	"""
	Nettoyage du contenu de l'attribut title qui peut contenir des balises <b> ou <i> qui posent problème ensuite à TXM.
	"""
	title_value = match.group(1) #Valeur de l'attribut title
	cleaned = patron_balises.sub("", title_value) #Supprime les balises en trop
	return f'title="{cleaned}"'

def add_attribut(match):
	"""
	Ajoute le nouvel attribut à la fin de la balise text (s'il n'existe pas déjà).
	Si changer_date = True, on ajoute aussi deux attributs de date (s'ils n'existent pas déjà).
	"""
	debut_balise_text = match.group(1) # Balise text dans le chevron fermant
	attributs = [] # Liste des attibuts à ajouter
	
	if ajouter_attribut: # Si on veut ajouter des attributs
		for new_attribut_nom,new_attribut_valeur in new_attributs.items(): # Pour chaque attribut de la liste (même si c'est une liste de 1)
			new_attribut = f'{new_attribut_nom}="{new_attribut_valeur}"' # Format de l'attribut à coller dans le fichier de sortie
			patron_new_attribut = re.compile(rf'\b{new_attribut_nom}\s*=') # Nom du nouvel attribut suivi de =
			if not patron_new_attribut.search(debut_balise_text): # S'il n'existe pas déjà dans la balise text
				attributs.append(new_attribut) # Ajoute le nouvel attribut à la liste
		
	if changer_date: # Si on veut modifier les dates 
		if 'annee=' not in debut_balise_text and 'mois=' not in debut_balise_text: #et que les attributs annee et mois ne sont pas déjà dans text
			date_match = patron_date.search(debut_balise_text) # On les cherche dans la balise text
			if date_match: # Si on match le bon format
				yyyy, mm, dd = date_match.groups() # On récupère les éléments de la date dans des variables différentes
				attributs.append(f'annee="{yyyy}"')
				attributs.append(f'mois="{yyyy}-{mm}"')
	
	if attributs: #S'il y a des attributs dans la liste
		return f'{debut_balise_text} {" ".join(attributs)}>'
	else:
		return match.group(0)

# Compteurs
nb_attr = 0
nb_clean = 0
nb_date = 0
	
# Pour chaque fichier xml du répertoire
for xml_file in repertoire_xml.glob("*.xml"):
	content = xml_file.read_text(encoding="utf-8") # Contenu du fichier
	new_content = content
	
	# Initialisation des actions réalisées
	nettoye = False
	attribut = False
	date_modif = False
	
	# Nettoyage title
	if nettoyer_titre: # Si la fonctionnalité de nettoyage est activée
		temp = patron_title.sub(clean_title, new_content) 
		if temp != new_content: # Et que title a été nettoyé
			nettoye = True
			new_content = temp # On met à jour le contenu du fichier avec
			nb_clean += 1
	
	# Ajout des attributs
	temp = patron_text.sub(add_attribut, new_content)
	if temp != new_content: 
		new_content = temp
		if ajouter_attribut: # Si la fonctionnalité d'ajout d'attribut est activée
			attribut = True
			nb_attr += 1
		if changer_date: # Si la fonctionnalité de changement de date est activée
			date_modif = True
			nb_date += 1
	
	if nettoye or attribut or date_modif: # Si une modification du fichier a eu lieu
		xml_file.write_text(new_content, encoding="utf-8") # On éccrit le nouveau contenu dans le fichier (on écrase le fichier d'origine - penser à garder le .zip quelque part si besoin)
		if nettoye: # S'il y a eu nettoyage (peu de fichiers normalement)
			print(f"{xml_file.name} nettoyé") # On affiche le nom du fichier
			
# Résultats			
if nettoyer_titre:
	print(f"Fichiers nettoyés : {nb_clean}")		
if ajouter_attribut:
	print(f"Attribut {new_attribut} ajouté dans {nb_attr} fichiers")
if changer_date:
	print(f"Dates modifiées dans {nb_date} fichiers")		
	