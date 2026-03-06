# Europresse_PCS_XML2TXM
Pré-traitements utiles pour préparer un corpus Europresse XML/XTZ récolté avec le Press Corpus Scraper afin de l'importer dans TXM.

Plusieurs fonctionnalités peuvent être appliquées à un répertoire qui contient les fichiers XML : 
- Nettoyage : il y a parfois des balises \<b> et \</b> dans l'attribut title de l'élément text (vu avec Sud_Ouest_auteurinconnu)
- Ajouter un attribut : pour faire un corpus partitionné selon des critères autres que ceux qui sont présents en attribut de text (source, author, title, date), on peut récolter des sous-corpus et y ajouter l'attribut qui correspond (ex : couverture, tonalité, pays, langue, etc.).
- Date : la date est au format aaaa/mm/dd, on peut aussi ajouter un attribut date_annee (yyyy) et un attribut date_mois (yyyy-mm) pour les corpus dont la couverture temporelle est étendue. 
