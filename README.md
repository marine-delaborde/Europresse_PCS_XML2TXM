# Europresse_PCS_XML2TXM
Pré-traitements utiles pour préparer un corpus Europresse XML/XTZ récolté avec le Press Corpus Scraper afin de l'importer dans TXM.

Plusieurs fonctionnalités peuvent être appliquées à un répertoire qui contient les fichiers XML : 
- **Nettoyage** : il y a parfois des balises \<b> et \</b> dans l'attribut title de l'élément text (vu avec Sud_Ouest_auteurinconnu), ce script les supprime.
- **Ajouter un attribut** (ou une liste d'attributs) : pour faire un corpus partitionné selon des critères autres que ceux qui sont présents en attribut de text (source, author, title, date), on peut récolter des sous-corpus selon une recherche Europresse. Ce script permet d'ajouter l'attribut (ou la liste d'attributs) qui correspond à cette recherche (ex : couverture, tonalité, pays, langue, etc.). Attention à ne pas mettre de _ dans le nom des attributs, ni d'accent. 
- **Date** : la date est au format aaaa/mm/dd. Ce script permet d'ajouter un attribut annee (yyyy) et un attribut mois (yyyy-mm) pour les corpus dont la couverture temporelle est étendue. 

Ces trois fonctionnalités sont activables ou non au début du script. 