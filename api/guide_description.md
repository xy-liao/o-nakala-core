# Guide de description - Documentation de l'infrastructure Huma-Num

https://documentation.huma-num.fr/nakala-guide-de-description/#:~:text=Guide%20pour%20d%C3%A9crire%20des%20donn%C3%A9es,%2C%20accessibles%2C%20interop%C3%A9rables%20et%20r%C3%A9utilisables.

[Documentation de l'infrastructure Huma-Num](https://documentation.huma-num.fr/)

# Guide pour décrire des données dans NAKALA[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#guide-pour-decrire-des-donnees-dans-nakala)

La qualité et la richesse de la description des données sont des critères centraux des principes [FAIR](https://doranum.fr/enjeux-benefices/principes-fair/). Cela constitue un moyen d’atteindre les objectifs visés : faire en sorte que les données soient faciles à trouver, accessibles, interopérables et réutilisables.

La qualité se met en oeuvre, par exemple :

- en utilisant des référentiels standardisés
- en respectant les mêmes normes intellectuelles de description pour un ensemble de données
- en choisissant les champs de métadonnées les plus adaptés à l’information donnée

La richesse se met en oeuvre en complétant le plus grand nombre possible de champs afin d’optimiser la compréhension des données.

Dans NAKALA, la description est basée sur un ensemble minimal de cinq informations qui peuvent être enrichies de manière étendue et cumulative.

L’objet de ce guide est de documenter le schéma général de description proposé par NAKALA pour aider à sa compréhension et à son utilisation afin d’en permettre une meilleure exploitation par les déposants.

En amont du dépôt, il peut s’avérer utile de définir ce qui doit être décrit :

- objet source
- fichier numérique
- objet numérisé
- objet représenté sur un support numérique

Un autre élément à prendre en compte est l’organisation des données de recherche à déposer. Dépose-t-on un fichier par dépôt ou plusieurs fichiers pour une même donnée ?

Ces choix auront en effet une incidence sur la description de la donnée et les informations renseignées, en particulier sur les métadonnées concernant le type de la donnée, la date de création, les auteurs, la description.

Ces choix doivent faire l’objet d’une réflexion scientifique afin que la gestion du dépôt et la description des données liées à un projet de recherche soient cohérents. Ces choix pourront par ailleurs être explicités dans le dépôt et/ou le projet.

Si l’on prend l’exemple de cette image : https://data.bnf.fr/ark:/12148/cb12074651d, les enjeux scientifiques et les pratiques de description ne seront pas identiques si l’on choisit de décrire :

- L’œuvre peinte par Robert Delaunay en 1910
- La photographie de la peinture réalisée par Kristopher McKay
- La tour de Gustave Eiffel dont l’image serait alors une ‘simple’ illustration

La description des collections dans NAKALA suit les mêmes principes et utilise le même modèle que les données. La principale différence est que les métadonnées obligatoires sont limitées au Statut de la collection (privé ou public) et au Titre.

## Sommaire[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#sommaire)

- [Zone “Métadonnées principales du dépôt”](https://documentation.huma-num.fr/nakala-guide-de-description/#zone-metadonnees-principales-du-depot)
    - [Type de dépôt (obligatoire)](https://documentation.huma-num.fr/nakala-guide-de-description/#type-de-donnees-obligatoire)
    - [Auteurs (obligatoire)](https://documentation.huma-num.fr/nakala-guide-de-description/#auteurs-obligatoire)
- [Zone “Informations complémentaires”](https://documentation.huma-num.fr/nakala-guide-de-description/#zone-informations-complementaires)
- [Zone “Ajouter d’autres métadonnées”](https://documentation.huma-num.fr/nakala-guide-de-description/#zone-ajouter-dautres-metadonnees)
    - [Propriétés du Dublin Core qualifié](https://documentation.huma-num.fr/nakala-guide-de-description/#proprietes-du-dublin-core-qualifie)

## Avertissement et guide à télécharger[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#avertissement-et-guide-a-telecharger)

La version actuelle du guide propose un ensemble de conseils et bonnes pratiques pour les champs de métadonnées obligatoires et complémentaires de premier niveau.

Ce guide a été mis à jour en **mars 2024**.

En complément de ce guide de description détaillé, un [**guide de dépôt de 2 pages au format PDF**](https://documentation.huma-num.fr/media/nakala/Guide_depot_Nakala_mars-2024.pdf) fournit des recommandations sur les fichiers et une présentation synthétique des principaux champs de description pour faciliter leur utilisation.

## Schéma général de description d’une donnée de NAKALA[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#schema-general-de-description-dune-donnee-de-nakala)

Le schéma de description est composé de :

- 5 propriétés nakala obligatoires (on parle de propriétés ‘maison’ – propriétés nkl) qu’on retrouve dans la zone “Métadonnées principales du dépôt” du formulaire de dépôt
- toutes les propriétés du schéma Dublin Core qualifié – propriétés dcterms – dans les zones “Informations complémentaires” et “Ajouter d’autres métadonnées” du formulaire de dépôt
- du schéma de description DataCite – propriétés RelationType – dans la zone “Relations vers d’autres données publiées dans NAKALA” du formulaire de dépôt

Aux cinq champs obligatoires de la notice de description de NAKALA (propriétés nakala), il est donc possible d’ajouter et dupliquer tout autre champ issu du vocabulaire [Dublin Core qualifié](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) qui est à disposition dans les zones “Informations complémentaires” et “Ajouter d’autres métadonnées”.

La description des données doit être la plus riche, précise et exacte possible. En complément des champs obligatoires, il est donc fortement recommandé d’enrichir la description par toute autre information connue sur la donnée.

### Dublin Core qualifié[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#dublin-core-qualifie)

Le vocabulaire [Dublin Core qualifié](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) (“DC”) est composé de :

1. une base (“DC simple”) de quinze propriétés de description très génériques : `contributor`, `coverage`, `creator`, `date`, `description`, `format`, `identifier`, `language`, `publisher`, `relation`, `rights`, `source`, `subject`, `title`, `type`
2. une extension (“DC qualifié”) comportant
    - des propriétés supplémentaires : `audience`, `provenance`, `rightsHolder`, etc.
    - des qualificatifs de raffinement permettant de préciser les propriétés de base. Par exemple : `available`, `created`, `dateAccepted`, `dateCopyrighted`, `dateSubmitted`, `issued`, `modified`, `valid` qui sont tous des qualificatifs venant préciser la notion générique de date.
    - des schémas d’encodage et des vocabulaires contrôlés pour exprimer les valeurs d’une propriété. Par exemple: `DCMIType`, `W3CDTF`, etc.

Pour d’autres vocabulaires : la possibilité d’implémenter dans son interface de dépôt un autre format que le Dublin Core n’est pas possible dans NAKALA. Le déposant peut néanmoins associer dans les fichiers d’une donnée, un fichier de métadonnées propre dans le format et le vocabulaire de son choix. Dans ce cas d’usage, il est possible d’exploiter cette description spécifique dans une exposition web externe à NAKALA.

### Schéma DataCite - propriétés RelationType[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#schema-datacite-proprietes-relationtype)

Dans la zone “Relations vers d’autres données publiées dans NAKALA”, les propriétés [RelationType du schéma DataCite](https://datacite-metadata-schema.readthedocs.io/en/4.5/appendices/appendix-1/relationType/) sont mises à disposition pour spécifier le type de relations **entre des données publiques déposées dans NAKALA**.

Pour des précisions sur la mise en relation de données NAKALA, consulter le paragraphe [“Créer des relations”](https://documentation.huma-num.fr/nakala-guide-de-description/#creer-des-relations).

Pour décrire des relations **entre la donnée NAKALA et des ressources externes**, on recommande les propriétés du Dublin Core qualifié accessibles dans la zone “Ajouter d’autres métadonnées” en sélectionnant dans le champ `Propriété` :

- la propriété générique `dcterms:relation`
- ou une de ses sous-propriétés qui spécifient plus finement le type de relation et qui sont donc à privilégier.

Pour des précisions sur la mise en relation d’une donnée NAKALA avec des ressources externes, consulter le paragraphe [“Lien vers des ressources externes”](https://documentation.huma-num.fr/nakala-guide-de-description/#liens-vers-des-ressources-externes).

### Recommandations pour la description[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#recommandations-pour-la-description)

Nous recommandons :

- de privilégier l’emploi des termes du DC qualifié quand c’est possible plutôt que ceux du DC simple
- lorsque le contenu d’une propriété est exprimé dans une langue, préciser celle-ci à l’aide du champ `Pas d'information de langue`
- privilégier, là où c’est pertinent, l’utilisation de syntaxes formelles ou de vocabulaires contrôlés plutôt que l’emploi de textes libres (encodages liés au champ `Type` associé à une propriété)
- quand plusieurs informations de même nature doivent être précisées, utiliser plusieurs fois la même propriété en la dupliquant
- ne pas utiliser de système basé sur des caractères de type ‘séparateurs’.

Pour toutes questions, contacter [nakala@huma-num.fr](https://documentation.huma-num.fr/nakala-guide-de-description/nakala@huma-num.fr).

Note

Huma-Num soutient des réseaux d’experts données disciplinaires ou métiers via son réseau de [consortiums](https://www.huma-num.fr/les-consortiums-hn/) et dans les [relais en région que représentent les MSH](https://www.huma-num.fr/carte-des-relais-huma-num-dans-les-msh/). La réflexion sur la description des données devrait inclure autant que faire se peut une harmonisation disciplinaire dans le choix des vocabulaires et dans la façon de compléter les informations. Les réseaux sont présentés dans la rubrique “Consortiums et Réseaux” du [site Huma-Num](https://www.huma-num.fr/).

## Zone “Métadonnées principales du dépôt”[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#zone-metadonnees-principales-du-depot)

Les 5 métadonnées de la zone “Métadonnées principales du dépôt” sont à renseigner obligatoirement pour enregistrer une donnée. Ces 5 métadonnées obligatoires s’appuient sur des propriétés nakala – des propriétés ‘maison’ qui s’inspirent du DC. Ces propriétés nakala correspondent aux champs :

- Type de dépôt
- Titre
- Auteurs
- Date de création
- Licence

| Type de dépôt | Titre | Auteurs | Date de création | Licence |
| --- | --- | --- | --- | --- |
| nakala:type | nakala:title | nakala:creator | nakala:created | nakala:license |

*Correspondance entre les noms des champs obligatoires et les propriétés nakala*

Lorsque ces 5 métadonnées sont renseignées et que la donnée est publiée, un DOI est attribué automatiquement et instantanément. Cela offre un socle minimal indispensable pour signaler, partager et citer la donnée. Ainsi, les propriétés nakala qui sont obligatoires pour enregistrer la donnée répondent aux enjeux d’accessibilité et de définition du cadre de réutilisation de la donnée. Cependant, il s’agit d’une description minimale et ces métadonnées ne sont pas nécessairement suffisantes pour comprendre le contexte de production et de collecte, et ne permettront pas une indexation satisfaisante de la donnée.

Pour saisir les métadonnées dans les propriétés nakala : https://documentation.huma-num.fr/nakala/#zone-metadonnees-principales-du-depot

### Fonctionnement des propriétés nakala obligatoires[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#fonctionnement-des-proprietes-nakala-obligatoires)

| Label du champ | Equivalence propriétés nakala | Cardinalité | Fonctionnement | Précisions complémentaires |
| --- | --- | --- | --- | --- |
| Type de dépôt | nakala:type | Monovalué | Liste fermée : COAR, bibo, Survey Ontology |  |
| Titre | nakala:title | Multivalué | Texte libre ; renseigner la langue de chaque titre | Champ multilingue |
| Auteurs | nakala:creator | Multivalué | Format contraint : Nom, Prénom - ORCID optionnel |  |
| Date de création | nakala:created | monovalué | Format contraint : AAAA-MM-JJ ou AAAA-MM ou AAAA | Spécifications du [W3C-DTF](https://www.w3.org/TR/NOTE-datetime) |
| Licence | nakala:license | monovalué | Liste fermée : Etalab, Creative Commons, GNU, FLOSS, Rights Statement, etc. |  |

### Type de dépôt (obligatoire)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#type-de-depot-obligatoire)

Dans ce champ, sélectionner le type le plus approprié dans la liste afin de préciser le type principal de la donnée, en particulier pour une donnée multifichiers. Le type s’affiche sous forme d’icone dans la page de présentation de la donnée.

Si vous souhaitez apporter des précisions sur la nature ou le genre de la donnée et renseigner un type qui décrit plus finement votre donnée, reportez cette information dans la propriété `dcterms:type` (zone “Ajouter d’autres métadonnées”).

La liste des types disponibles dans le champ `Type de dépôt` est fermée. Elle est constituée de plusieurs référentiels dont le référentiel “Types” de [COAR](https://vocabularies.coar-repositories.org/resource_types/), la “Confederation of Open Access Repositories”.

Liste des types de données :

| Type | URI |
| --- | --- |
| image | http://purl.org/coar/resource_type/c_c513 |
| article de journal | http://purl.org/coar/resource_type/c_6501 |
| poster | http://purl.org/coar/resource_type/c_6670 |
| livre | http://purl.org/coar/resource_type/c_2f33 |
| set de données | http://purl.org/coar/resource_type/c_ddb1 |
| logiciel | http://purl.org/coar/resource_type/c_5ce6 |
| autre | http://purl.org/coar/resource_type/c_1843 |
| fonds d’archives | http://purl.org/library/ArchiveMaterial |
| exposition d’art | http://purl.org/ontology/bibo/Collection |
| bulletin | http://purl.org/ontology/bibo/Series |
| manuscrit | http://purl.org/coar/resource_type/c_0040 |
| correspondance | http://purl.org/coar/resource_type/c_0857 |
| périodique | http://purl.org/coar/resource_type/c_2659 |
| prépublication | http://purl.org/coar/resource_type/c_816b |
| article programmable | http://purl.org/coar/resource_type/c_e9a0 |

Lien

Requête API pour interroger la [liste des types](https://api.nakala.fr/vocabularies/datatypes) : `curl -X GET "https://api.nakala.fr/vocabularies/datatypes" -H  "accept: application/json"`

### Titre (obligatoire)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#titre-obligatoire)

Il s’agit de décrire la donnée par un titre ou un nom. Celui-ci devrait être précis et unique pour permettre au mieux de comprendre la donnée.

Il est recommandé de renseigner au moins un titre signifiant, sur le modèle d’un titre d’article pour faciliter l’indexation de la donnée et sa recherche. Selon les besoins et usages des données concernées, le titre pourra comporter des mentions de date, de lieu, de personnes, etc.

Le champ `Titre` (`nkl:title`) est répétable afin, par exemple, de l’indiquer en différentes langues. Le premier titre enregistré sera affiché en tête de la page de présentation.

Renseigner systématiquement la langue de chaque titre dans le champ associé intitulé “Pas d’information de langue”.

Pour renseigner un titre secondaire, un titre abrégé ou un autre nom donné à la ressource, privilégier la propriété `dcterms:alternative` (zone “Ajouter d’autres métadonnées”).

Note

Le titre de la donnée est différent du nom du ou des fichier.s associé.s dans le dépôt. Une donnée dans NAKALA est constituée d’une notice de description accompagnée d’un ou plusieurs fichiers. Le nommage des fichiers de données est également à organiser et à planifier. Des règles sont explicitées dans la partie [“Préparer les données”](https://documentation.huma-num.fr/nakala-preparer-ses-donnees/) du site de documentation de Huma-Num.

### Auteurs (obligatoire)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#auteurs-obligatoire)

Dans le champ `Auteurs` (`nkl:creator`), nous recommandons d’indiquer le producteur de la donnée. Cependant, cela n’est pas toujours adapté, ni possible (auteur inconnu), ni cohérent avec vos besoins.

Pour répondre aux différents besoins de description du rôle “Auteur”, plusieurs options sont proposées :

- Dans « Ajouter un auteur » : recherche par nom d’auteur pour vérifier si l’auteur est déjà enregistré dans la base Auteurs de NAKALA ; recherche par identifiant ORCID. Remarque : l’ORCID est une information optionnelle donc il est possible que l’auteur ait été enregistré sans son ORCID.
- Création de nouveaux auteurs
- Ajout d’un nombre d’auteurs sans limitation
- L’option de cocher « Anonyme » si l’auteur n’est pas connu sous la forme nom/prénom. Par exemple, si le producteur de donnée est une organisation, une institution ; que les informations sur l’auteur sont partielles ; que l’auteur est anonyme ; que les mentions de dates de naissance et de mort, le rôle, etc. doivent être renseignées…
- Ajout d’auteurs sous une autre forme que nom/prénom dans la propriété `dcterms:creator` (zone “Ajouter d’autres métadonnées”) ou toute autre personne qui a contribué à la production et à la collecte de la donnée dans `dcterms:contributor`.

Lors de la saisie, des noms d’auteurs s’affichent par autocomplétion. Si aucun auteur de la liste ne correspond, vous avez la possibilité d’ajouter de nouveaux auteurs. La base ‘Auteurs’ de NAKALA est enrichie au fur et à mesure par les utilisateurs.

**Pour créer un nouvel auteur, il faut obligatoirement renseigner un prénom et un nom**. Renseigner l’ORCID de l’auteur est facultatif. Cependant, il est recommandé de vérifier que l’auteur a un identifiant ORCID et de renseigner l’ORCID de chaque auteur afin d’éviter tout ambigüité et confusion et d’attribuer la donnée à son auteur.

L’ORCID enregistré est contrôlé afin de vérifier sa forme (et éviter ainsi une erreur de saisie manuelle). Par ailleurs, un contrôle automatique permet de vérifier que cet ORCID n’a pas déjà été enregistré et associé à un autre auteur dans NAKALA.

Pour l’instant, il n’est pas possible de mettre à jour une information sur un auteur déjà enregistré : contacter [nakala@huma-num.fr](https://documentation.huma-num.fr/nakala-guide-de-description/nakala@huma-num.fr).

### Auteurs, contributeurs, rôles, dates de vie et de mort, etc.[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#auteurs-contributeurs-roles-dates-de-vie-et-de-mort-etc)

**Si l’auteur à renseigner n’est pas de la forme ‘Nom, Prénom’**, cocher « Anonyme » et utiliser la propriété `dcterms:creator` du DC qualifié dans la zone “Ajouter d’autres métadonnées”. Par exemple, quand le producteur de donnée est une organisation, une institution, que vous avez des informations partielles ou a contrario plus riches à renseigner sur l’auteur, etc.

**Pour les personnes ayant participé à la production, à la collecte ou au traitement des données et qui n’en sont pas les auteurs**, il est également possible – et recommandé – de les mentionner dans des propriétés spécifiques du DC qualifié. En effet, dans “Ajouter d’autres métadonnées”, plusieurs propriétés se rapportent à la description d’un rôle sur une donnée pour répondre à un besoin plus large de description et de citation. Ainsi, pour renseigner des informations sur les entités qui ont participé à la production, la collecte, la création et la publication de la ressource, les propriétés du DC qualifié :

- `dcterms:creator`
- `dcterms:contributor`
- `dcterms:mediator`
- `dcterms:publisher`
- `dcterms:rightsHolder`

Dans ces propriétés, il est possible de saisir librement les informations sur les auteurs et contributeurs : établissement, organisation, institution, maison d’édition, nom partiel, rôle, dates, etc. Néanmoins, il est recommandé de définir une forme systématique qui sera appliquée à chaque auteur et contributeur de la donnée.

### Citation des `dcterms:creator`[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#citation-des-dctermscreator)

Si « Anonyme » a été coché et que vous renseignez chaque auteur dans un `dcterms:creator`, tous les auteurs seront affichés dans le bloc de citation de la donnée.

- Définir une liste des rôles adaptés à vos besoins
- Etablir une convention d’écriture pour mentionner l’entité et son rôle, les dates, etc. afin de l’appliquer systématiquement. Par exemple :
    - Nom, Prénom ; rôle
    - Nom, Prénom (1920-1990)

Ces solutions sont applicables aux propriétés `dcterms:creator` ;`dcterms:contributor` ; `dcterms:mediator` ; `dcterms:publisher` ; `dcterms:rightsHolder`.

Exemple 1 :

- nakala:creator (= champ Auteurs) : Evan Rees
- dcterms:creator : Rees, Evan (1850-1923)
- dcterms:contributor : Brasil. Ministério da guerra. Directoria do serviço geográfico

Exemple 2 :

- nakala:creator (= champ Auteurs) : Hélène Jouguet
- dcterms:creator : Jouguet, Hélène (transcriber)
- dcterms:contributor : Jacobson, Michel (speaker)
- dcterms:publisher : Huma-Num, UAR3598

### Date de création (obligatoire)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#date-de-creation-obligatoire)

Selon les projets et les objectifs scientifiques, il s’agira dans le champ `Date de création` (`nkl:created`) soit de mentionner la date de création du contenu de la ressource, soit la date de création de sa forme numérisée, en cas de numérisation a posteriori.

**Dans le champ `Date de création`, le format de la date à renseigner est contraint**. Ce champ accepte uniquement les formes suivantes du [W3C-DTF](https://www.w3.org/TR/NOTE-datetime) :

- YYYY-MM (année-mois). Exemple : 2024-03
- YYYY (année). Exemple : 2024

**Si vous avez des informations d’ordre temporel à renseigner qui ne correspondent pas à l’un de ces formats**, cochez « Inconnue ».

Pour renseigner d’autres types d’informations temporelles (sous forme textuelle, dates liées à différentes étapes du cycle de vie de la ressource, etc.), il est possible – et recommandé – de les mentionner dans des propriétés spécifiques du DC qualifié. Dans “Ajouter d’autres métadonnées”, plusieurs propriétés se rapportent à la description de ce type d’informations et acceptent des métadonnées sous forme libre : `dcterms:temporal` ; `dcterms:date` et ses sous-propriétés.

Les sous-propriétés de `dcterms:date` associées au cycle de vie de la ressource :

- `dcterms:available`
- `dcterms:created`
- `dcterms:dateAccepted`
- `dcterms:dateCopyrighted`
- `dcterms:dateSubmitted`
- `dcterms:issued`
- `dcterms:dateModified`
- `dcterms:valid`

### Licence (obligatoire)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#licence-obligatoire)

La licence renseignée précise les conditions de réutilisation des fichiers des données. Les métadonnées sont quant à elles sous la licence CC-BY afin de faciliter leur exposition (interopérabilité, moissonnage, référencement).

Le champ `Licence` (`nkl:licence`) permet de sélectionner :

Pour répondre à d’autres besoins, le champ `Licence` propose également une liste de 400 licences. Pour retrouver une licence, la recherche par autocomplétion a été mise en place. Saisir les premiers caractères du nom de la licence, des propositions remonteront automatiquement ; sélectionner la licence.

Pour des informations juridiques à renseigner autres que la licence, privilégier les propriétés DC (zone “Ajouter d’autres métadonnées”) : `dcterms:accessRights` ; `dcterms:rights`, `dcterms:rightsHolder`.

Requête API pour interroger la [liste des licences](https://api.nakala.fr/vocabularies/licenses) : `curl -X GET "https://api.nakala.fr/vocabularies/licenses" -H "accept: application/json"`

Voir la ressource de Doranum “[Les licences de réutilisation dans le cadre de l’Open data et de la loi pour une République numérique. Publié le 22/11/2018 | MAJ le 26/01/2023 | DOI : 10.13143/ssh2-zd93”](https://doranum.fr/aspects-juridiques-ethiques/les-licences-de-reutilisation-dans-le-cadre-de-lopen-data-2/).

## Zone “Informations complémentaires”[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#zone-informations-complementaires)

### 3 propriétés du Dublin Core[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#3-proprietes-du-dublin-core)

Les 3 métadonnées de la zone “Informations complémentaires” sont issues du Dublin Core. Elles sont optionnelles mais fortement recommandées car utiles à la compréhension de la donnée par des tierces personnes et elles offrent un premier niveau d’indexation satisfaisant.

| Description | Mots-clés | Langues |
| --- | --- | --- |
| dcterms:description | dcterms:subject | dcterms:language |

*Correspondance entre les noms des champs et les propriétés dcterms*

Pour saisir les métadonnées dans ces 3 champs : https://documentation.huma-num.fr/nakala/#zone-informations-complementaires

| Label du champ | Equivalence propriétés DC | Cardinalité | Fonctionnement | Précisions complémentaires |
| --- | --- | --- | --- | --- |
| Description | dcterms:description | Multivalué | Texte libre ; renseigner la langue |  |
| Mots-clés | dcterms:subject | Multivalué | Liste des labels issus des référentiels d’Isidore : RAMEAU, Pactols, GEMET, LCSH, BNE, GéoEthno, ArchiRès, Geonames ; Et/ou ajout manuel ; Renseigner la langue | Liste des référentiels d’Isidore : https://isidore.science/vocabularies |
| Langues | dcterms:language | Multivalué | Liste fermée de plus de 7 000 langues vivantes ou éteintes selon les normes [RFC5646](https://api.nakala.fr/vocabularies/languages?limit=10000) |  |

### Description (recommandé)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#description-recommande)

Le champ `Description` correspond à la propriété `dcterms:description` du Dublin Core.

Ce champ permet sous la forme d’un texte libre de décrire le contenu de la ressource, de préciser le contexte de production de la donnée, les méthodes et les protocoles d’obtention, les équipements utilisés, les variables, le projet de recherche, etc. Pour des enjeux documentaires, il est recommandé de créer un champ de description par ‘sujet’ de description et de renseigner la langue de chaque description dans le champ associé intitulé `Pas d’information de langue`.

Précisions sur le choix des champs de description issus du DC qualifié (zone “Ajouter d’autres métadonnées”) :

- Si la description est un résumé du projet de recherche, privilégier `dcterms:abstract`
- Si la description est une table des matières, privilégier `dcterms:tableOfContent`
- Renseigner systématiquement la langue de la description dans le champ associé intitulé `Pas d’information de langue`

### Mots-clés (recommandé)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#mots-cles-recommande)

Le champ `Mots-clés` correspond à la propriété `dcterms:subject` du DC.

Il permet de décrire le ou les sujet.s du contenu intellectuel de la ressource. Ce champ est très utile pour l’indexation de la donnée.

Lors de la saisie des premiers caractères d’un terme, l’autocomplétion propose une liste de labels des concepts issus des référentiels utilisés par [Isidore](https://isidore.science/vocabularies) : RAMEAU, Pactols, GEMET, LCSH, BNE, GéoEthno, ArchiRès, Geonames.

Cette autocomplétion constitue une aide au choix. Le déposant peut sélectionner un des labels qui est proposé mais également créer de nouveaux mots-clés. Pour cela, il suffit de saisir le terme et valider (touche Entrée) pour qu’il soit pris en compte.

Pour répondre à différents besoins, plusieurs possibilités sont proposées :

- renseigner la langue des mots-clés dans le champ associé intitulé `Pas d’information de langue`
- sélection d’un mot-clé suggéré par la liste ou ajout manuel
- champ répétable pour renseigner, par exemple, la même liste de mots-clés dans une autre langue
- 
    
    pour d’autres formes (identifiant et URI d’un concept) : sélection de la propriété `dcterms:subject` dans la zone “Ajouter d’autres métadonnées” pour renseigner :
    
    - un code (identifiant) d’un concept issu d’un référentiel encodé dans le DC qualifié. Deux référentiels sujets encodés dans le DC sont proposés dans NAKALA et adaptés à ce besoin : `dcterms:LCSH` ; `dcterms:TGN`. Pour utiliser ces deux encodages, saisir l’identifiant du concept dans `dcterms:subject` et dans le champ ‘Type’ associé, sélectionnez `dcterms:LCSH` ou `dcterms:TGN`.
        - Pour des précisions sur l’encodage `dcterms:LCSH`, consulter le paragraphe [“Encodage dcterms:LCSH (Library of Congress Subject Headings)](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermslcsh-library-of-congress-subject-headings)”.
        - Pour des précisions sur l’encodage `dcterms:TGN`, consulter le paragraphe [“Encodage dcterms:TGN (Getty Thesaurus of Geographic Names)](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermstgn-getty-thesaurus-of-geographic-names)”.
    - une URI qui pointe vers le concept d’un référentiel. Lorsqu’une URI est saisie, il est recommandé de typer ce lien afin que les machines soient capables de l’interpréter et que le lien soit dynamique et pointe directement vers le concept du référentiel. Pour cela, sélectionner dans le champ `Type` associé à la propriété `dcterms:subject`, l’encodage `dcterms:URI`.
        - Pour des précisions sur l’encodage `dcterms:URI`, consulter le paragraphe [“Encodage `dcterms:URI` (lien web)](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsuri-lien-web)”.

### Langues (recommandé)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#langues-recommande)

Le champ `Langues` correspond à la propriété `dcterms:language` du DC.

**Il s’agit ici de renseigner la langue du contenu du ou des fichier.s. Cette métadonnée s’applique donc aux fichiers textuels, vidéos, sonores**.

L’identification de la langue se fait en recherchant par autocomplétion dans le référentiel de NAKALA. Le référentiel des langues implémenté dans le champ `Langues` est issu d’une liste fermée de plus de 7 000 langues vivantes ou éteintes de la norme [RFC5646](https://api.nakala.fr/vocabularies/languages?limit=10000).

Il est également possible d’utiliser le champ `dcterms:language` (zone “Ajouter d’autre métadonnées”) pour renseigner une langue qui ne serait pas proposée dans le référentiel ou pour enrichir l’information, par exemple pour préciser l’écriture utilisée : [code ISO-15924](https://fr.wikipedia.org/wiki/ISO_15924#).

## Zone “Ajouter d’autres métadonnées”[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#zone-ajouter-dautres-metadonnees)

### Propriétés du Dublin Core qualifié[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#proprietes-du-dublin-core-qualifie)

Pour enrichir la description, toutes les propriétés du Dublin Core qualifié sont disponibles dans la zone “Ajouter d’autres métadonnées”.

Pour saisir une métadonnée dans cette zone : https://documentation.huma-num.fr/nakala/#zone-ajouter-dautres-metadonnees.

Pour des précisions sur le schéma Dublin Core qualifié, consulter :

- les différentes alternatives spécifiées dans ce guide

## Créer des relations[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#creer-des-relations)

### Zone “Relations vers d’autres données publiées dans NAKALA”[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#zone-relations-vers-dautres-donnees-publiees-dans-nakala)

Dans la zone “Relations vers d’autres données publiées dans NAKALA”, les propriétés sont issues du schéma ‘RelationType’ de DataCite : https://datacite-metadata-schema.readthedocs.io/en/4.5/appendices/appendix-1/relationType/.

Cette zone permet de déclarer et créer des relations symétriques entre des données publiques déposées dans NAKALA. Ainsi, pour utiliser cette fonctionnalité et créer une relation entre une donnée A et une donnée B déposées dans NAKALA, les deux données devront avoir le statut « public ».

La liste de propriétés ‘RelationType’ permet de préciser le type de relation qui existe entre deux données NAKALA publiques par des liens explicites sémantiquement et de faciliter la mise en relation. Lorsque vous avez établi une relation entre la donnée A et une donnée B, la donnée B pointera automatiquement vers la donnée A en affichant la relation symétrique :

- IsCitedBy ; Cites
- IsSupplementTo ; IsSupplementedBy
- IsContinuedBy ; Continues
- Describes ; IsDescribedBy
- HasMetadata ; IsMetadataFor
- HasVersion ; IsVersionOf
- IsNewVersionOf ; IsPreviousVersionOf
- IsPartOf; HasPart; IsPublishedIn
- IsReferencedBy ; References
- IsDocumentedBy ; Documents
- IsCompiledBy ; Compiles
- IsVariantFormOf ; IsOriginalFormOf
- IsIdenticalTo
- IsReviewedBy ; Reviews
- IsDerivedFrom ; IsSourceOf
- IsRequiredBy ; Requires
- Obsoletes ; IsObsoletedBy
- IsCollectedBy ; Collects

Pour saisir les métadonnées dans cette zone : https://documentation.huma-num.fr/nakala/#zone-relations-vers-dautres-donnees-publiees-dans-nakala.

Si des relations sur des données dont vous avez la responsabilité avaient été ajoutées par une tierce personne et que ces relations étaient sujettes à questionnement, nous contacter sur [nakala@huma-num.fr](https://documentation.huma-num.fr/nakala-guide-de-description/nakala@huma-num.fr). L’équipe Nakala sera en mesure, le cas échéant, de retirer la relation symétrique qui a été générée automatiquement.

### Liens vers des ressources externes[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#liens-vers-des-ressources-externes)

Pour établir des relations entre une donnée et des ressources externes (base de données, bibliothèques numériques, sites web, etc.), il est recommandé de renseigner les liens web (URL et URI) des ressources dans `dcterms:relation` ou ses sous-propriétés (zone “Ajouter d’autres métadonnées”). Les sous-propriétés sont à privilégier car elles caractériseront plus précisément le type de relation entre les ressources (si applicable) :

- dcterms:relation
- dcterms:conformsTo
- dcterms:hasFormat
- dcterms:isFormatOf
- dcterms:hasPart
- dcterms:isPartOf
- dcterms:hasVersion
- dcterms:isVersionOf
- dcterms:isReferencedBy
- dcterms:references
- dcterms:isReplacedBy
- dcterms:replaces
- dcterms:isRequiredBy
- dcterms:requires
- dcterms:source

Si vous renseignez uniquement les liens web qui pointent vers les ressources, nous recommandons de sélectionner dans le champ `Type` associé à la propriété ‘relation’ de votre choix, l’encodage `dcterms:URI`.

Les machines seront alors capables d’interpréter ce lien web et de le rendre dynamique : il pointera automatiquement vers la ressource web externe. Pour cela, Pour des précisions sur l’encodage `dcterms:URI`, consulter le paragraphe [“Encodage `dcterms:URI` (lien web)](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsuri-lien-web)”.

## Champ `Type` pour encoder les valeurs d’une propriété[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#champ-type-pour-encoder-les-valeurs-dune-propriete)

Le schéma de description DC qualifié prévoit des encodages qui permettent d’identifier la valeur de l’information renseignée, c’est-à-dire que l’on va préciser que l’information contenue dans la métadonnée représente une ‘chaîne de caractères’, un ‘nombre’, une ‘date’, des ‘coordonnées géographiques’, une ‘URI’, etc.

Typer certaines métadonnées avec un encodage adapté permet aux machines d’interpréter sémantiquement ou techniquement l’information et de la restituer correctement. Le partage de l’information avec d’autres machines est alors facilité et convenablement exploité. Par défaut, l’encodage de base pour chaque propriété dans NAKALA est `string` qui signifie que l’information contenue dans la métadonnée est une simple chaîne de caractères. Dans NAKALA, une sélection d’encodages du DC qualifié a été mise à disposition.

Ces encodages ne peuvent être utilisés qu’en association avec une propriété du DC qualifié. Ainsi, lorsque vous avez sélectionné la propriété adaptée au contenu intellectuel de la métadonnée saisie, il vous sera possible de choisir un encodage spécifique dans le champ `Type` pour préciser la forme de la valeur contenue dans la propriété.

Seuls certains encodages seront utiles et adaptés aux données, à la discipline et au projet de recherche. Ces encodages doivent donc être utilisés dans un objectif précis et adaptés au type d’information contenue dans la métadonnée. Il faut donc définir en amont de toute utilisation de ces encodages les besoins scientifiques et documentaires et vérifier s’ils sont applicables et pertinents.

Dans la majorité des cas, lorsqu’un encodage est sélectionné, ne pas renseigner le champ `Pas d'information de langue`.

La propriété caractérise intellectuellement l’information ; l’encodage caractérise techniquement la valeur de l’information contenue dans la propriété.

Dans NAKALA, une sélection d’encodages du DC qualifié a été implémentée :

- `dcterms:DCMIType` : enncodage d’une liste fermée de 12 valeurs qui définit le type de la ressource numérique
- `dcterms:LCSH` : encodage des concepts du référentiel d’autorité-matière de la *Library of Congress*
- `dcterms:TGN` : encodage des concepts du référentiel du *Getty Thesaurus of Geographic Names*
- `dcterms:Box` : encodage des espaces géographiques délimités
- `dcterms:ISO3166` encodage des codes pays issus de la norme ISO 3166
- `dcterms:RFC5646` : encodage des codes de représentation des langues issu de la spécification RFC-5646
- `dcterms:Period` : encodage d’intervalles temporels délimités
- `dcterms:Point` : encodage des coordonnées géographiques
- `dcterms:URI` : encodage des liens web
- `dcterms:W3CDTF` : encodage des dates selon le standard du W3C-DTF

Chacun de ces encodages est normalisé, cela signifie que les informations saisies doivent correspondre à une valeur du référentiel ou respecter une forme particulière pour permettre aux machines de les interpréter correctement et donc de les exploiter.

Les encodages `dcterms:DCMIType`, `dcterms:LCSH` et `dcterms:TGN` sont labellisés comme « Vocabulary Encoding Scheme » dans le schéma DC et sont liés à des vocabulaires contrôlés internes ou externes au DC : https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-4.

Quant aux autres encodages conservés dans NAKALA, il s’agit de « Syntax Encoding Schemes ». Leur utilisation est contrainte à une syntaxe spécifique documentée dans le schéma DC : https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-5.

### Encodage `dcterms:DCMIType` (type de la ressource)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsdcmitype-type-de-la-ressource)

L’encodage `dcterms:DCMIType` doit être strictement associé à la propriété `dcterms:type`.

`dcterms:DCMIType` encode le *DCMI Type Vocabulary*, un vocabulaire contrôlé mis en place par la *Dublin Core Metadata Initiative* dont la définition est :

< [The set of classes specified by the DCMI Type Vocabulary, used to categorize the nature or genre of the resource](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/DCMIType).

**`dcterms:DCMIType` est associé à une liste fermée de 12 valeurs**. Lorsque l’on utilise ce type, il faut donc renseigner obligatoirement une valeur issue de ce vocabulaire : https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-7.

Pour utiliser cet encodage dans NAKALA, sélectionner la propriété `dcterms:type` (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:DCMIType` et saisir une des valeurs listées ci-dessous. Ne rien renseigner dans le champ `Pas d'information de langue`.

**Liste des valeurs acceptées pour `dcterms:DCMIType`** :

- Collection
- Dataset
- Event
- Image
- InteractiveResource
- MovingImage
- PhysicalObject
- Service
- Software
- Sound
- StillImage
- Text

Un exemple d’utilisation de l’encodage `dcterms:DCMIType` associé à `dcterms:type` : https://nakala.fr/10.34847/nkl.2a094h08.

### Encodage `dcterms:LCSH` (Library of Congress Subject Headings)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermslcsh-library-of-congress-subject-headings)

L’encodage `dcterms:LCSH` doit être strictement associé à la propriété `dcterms:subject`.

`dcterms:LCSH` – *Library of Congress Subject Headings* – encode les autorité-matière (sujets) de la *Library of Congress*. La définition de cet encodage dans le DC :

< [The set of labeled concepts specified by the Library of Congress Subject Headings](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/LCSH).

Pour utiliser cet encodage, dans NAKALA, sélectionner la propriété `dcterms:subject` (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:LCSH`. Ne rien renseigner dans le champ `Pas d'information de langue`.

**Pour l’encodage `dcterms:LCSH`, plusieurs solutions existent dans NAKALA**. Vous pouvez renseigner pour un mot-clé issu du référentiel LCSH :

- l’identifiant du concept
- le label du concept
- l’URI qui pointe vers le concept du LCSH

Si vous souhaitez renseigner l’identifiant, le label et l’URI d’un même mot-clé, il est recommandé de créer un nouveau `dcterms:subject` pour chaque type d’information.

Pour les concepts LCSH, consulter : https://id.loc.gov/authorities/subjects.html ou https://id.loc.gov/search/.

Un exemple d’utilisation de l’encodage `dcterms:LCSH` associé à `dcterms:subject` : https://nakala.fr/10.34847/nkl.3f9b2i11.

### Encodage `dcterms:TGN` (Getty Thesaurus of Geographic Names)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermstgn-getty-thesaurus-of-geographic-names)

L’encodage `dcterms:TGN` peut être associé à deux propriétés :

- `dcterms:subject`
- `dcterms:spatial`

`dcterms:TGN` encode les concepts du *Thesaurus of Geographic Names* du *Getty Research Institute*. Sa définition dans le DC :

< [The set of places specified by the Getty Thesaurus of Geographic Names](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/TGN).

Pour utiliser cet encodage, dans NAKALA, sélectionner la propriété `dcterms:subject` ou `dcterms:spatial` (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:TGN`. Ne rien renseigner dans le champ `Pas d'information de langue`.

**Pour l’encodage `dcterms:TGN`, il est recommandé de renseigner l’identifiant du concept du TGN**.

Un exemple d’utilisation de l’encodage `dcterms:TGN` associé à `dcterms:spatial` : https://nakala.fr/10.34847/nkl.a8acx43q.

### Encodage `dcterms:Box` (espace géographique délimité)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsbox-espace-geographique-delimite)

L’encodage `dcterms:Box` doit être strictement associé à la propriété `dcterms:spatial`.

`dcterms:Box` sert à encoder les limites géographiques d’un espace physique selon le schéma d’encodage du DCMI :

< [The set of regions in space defined by their geographic coordinates according to the DCMI Box Encoding Scheme](https://www.dublincore.org/specifications/dublin-core/dcmi-box/).

Le Dublin Core définit des règles de syntaxe associées à l’encodage `dcterms:Box`. Dans NAKALA, ces règles ont été adaptées. Pour utiliser cet encodage dans NAKALA, sélectionner la propriété `dcterms:spatial` (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:Box`. Ne rien renseigner dans le champ `Pas d'information de langue`.

**Dans NAKALA, les composants à utiliser pour `dcterms:Box` sont** :

- northlimit : obligatoire
- southlimit : obligatoire
- eastlimit : obligatoire
- westlimit : obligatoire
- uplimit : facultatif
- downlimit : facultatif
- name : facultatif
- units : facultatif
- zunits : facultatif
- projection : facultatif

**Les règles à suivre** :

- northlimit et southlimit : obligatoire et compris entre [-90 à +90]
- eastlimit et westlimit : obligatoire et compris entre [-180 à 180]
- uplimit doit être compris entre [-6 371 000 et 8 849]
- downlimit doit être compris entre [-6 371 000 et 8 849] et inférieur à uplimit, si uplimit est renseigné
- units : la seule valeur acceptée est “signed decimal degrees”
- zunits : la seule valeur acceptée est “metres”. Ne peut être ajouté que si uplimit ou downlimit est renseigné
- projection : la seule valeur acceptée est “WGS84”

Quelques exemples :

- northlimit=-7.73; southlimit=-12; westlimit=42; eastlimit=48.29
- westlimit=-7.22; southlimit=34.67; eastlimit=45.99; northlimit=58.54
- northlimit=48.9354; southlimit=47.2479; westlimit=-4.8504; eastlimit=-0.9722

Un exemple d’utilisation de l’encodage `dcterms:Box` associé à `dcterms:spatial` : https://nakala.fr/10.34847/nkl.92d01y93.

### Encodage `dcterms:ISO3166` (code pays)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsiso3166-code-pays)

L’encodage `dcterms:ISO3166` doit être strictement associé à la propriété `dcterms:spatial`.

`dcterms:ISO3166` sert à encoder les codes pays de la norme ISO 3166 :

< [a pour but de définir des codes internationalement reconnus de lettres et/ou de chiffres qui peuvent être utilisés pour désigner des pays et leurs subdivisions](https://www.iso.org/fr/iso-3166-country-codes.html).

Pour utiliser cet encodage dans NAKALA, sélectionner la propriété `dcterms:spatial` (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:ISO3166`. Ne rien renseigner dans le champ `Pas d'information de langue`.

**Dans NAKALA, le choix du code alpha-2 (code pays sur 2 caractères) a été établi pour renseigner le code pays associé à dcterms:ISO3166**. Il couvre l’ensemble des pays et est donc le plus complet.

Pour retrouver le code d’un pays issu de la norme ISO3166, consulter la page suivante et sélectionner sur l’interface, le filtre CountryCode : https://www.iso.org/obp/ui/#search.

Un exemple d’utilisation de l’encodage `dcterms:ISO3166` associé à `dcterms:spatial` : https://nakala.fr/10.34847/nkl.b97f0454.

### Encodage `dcterms:RFC5646` (codes langues)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsrfc5646-codes-langues)

L’encodage `dcterms:RFC-5646` du Dublin Core peut être associé à deux propriétés :

- `dcterms:subject`
- `dcterms:language`

Pour l’instant seule la sous-étiquette `language` de la norme RFC-5646 est autorisée dans Nakala afin d’identifier une langue.

Pour utiliser cet encodage dans NAKALA, sélectionner la propriété `dcterms:subject` ou `dcterms:language` (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:RFC-5646`. Ne rien renseigner dans le champ `Pas d'information de langue`.

Pour retrouver les codes des langues, consulter l’API de Nakala https://api.nakala.fr/vocabularies/languages?limit=10000 ou directement le [registre de IANA](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry).

### Encodage `dcterms:Period` (intervalle temporel délimité)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsperiod-intervalle-temporel-delimite)

L’encodage `dcterms:Period` peut être associé à deux propriétés :

- `dcterms:temporal`
- `dcterms:date` et ses sous-propriétés

`dcterms:Period` sert à encoder un intervalle temporel délimité selon le schéma d’encodage du DCMI :

< [The set of time intervals defined by their limits according to the DCMI Period Encoding Scheme](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/Period).

Pour utiliser cet encodage dans NAKALA, sélectionner la propriété `dcterms:temporal` ou `dcterms:date` et ses sous-propriétés (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:Period`. Ne rien renseigner dans le champ `Pas d'information de langue`, sauf si des métadonnées textuelles étaient renseignées dans le composant ‘name’.

**Dans NAKALA, les composants à utiliser pour `dcterms:Period` sont** :

- name (facultatif)
- start (obligatoire)
- end (obligatoire)

**Les règles à suivre** :

- les années doivent comporter au moins 4 chiffres. Par exemple : start=0030; end=0330
- les années peuvent être négatives : start=-0330; end=-0030
- la date saisie dans ‘start’ doit être antérieure à la date saisie dans ‘end’

Des exemples de syntaxes :

- name=Hellénistique, Antiquité; start=-0330; end=-0030
- name=Paléolithique; start=-300000; end=-40000
- name=The Great Depression; start=1929; end=1939
- start=1999-09-25T14:20+10:00; end=1999-09-25T16:40+10:00

Un exemple d’utilisation de l’encodage `dcterms:Period` associé à une sous-propriété de `dcterms:date` : https://nakala.fr/10.34847/nkl.f55a7ml5.

### Encodage `dcterms:Point` (coordonnées géographiques)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermspoint-coordonnees-geographiques)

L’encodage `dcterms:Point` doit être strictement associé à la propriété `dcterms:spatial`.

`dcterms:Point` sert à encoder des coordonnées géographiques selon le schéma d’encodage du DCMI :

< [The set of points in space defined by their geographic coordinates according to the DCMI Point Encoding Scheme](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/Point).

Pour utiliser cet encodage dans NAKALA, sélectionner la propriété `dcterms:spatial` (zone “Ajouter d’autres métadonnées”) puis dans le champ `Type`, sélectionner `dcterms:Point`. Ne rien renseigner dans le champ `Pas d'information de langue`, sauf si des métadonnées textuelles étaient renseignées dans le composant ‘name’.

**Dans NAKALA, les composants à utiliser pour `dcterms:Point` sont** :

- east : obligatoire
- north : obligatoire
- elevation : facultatif
- name : facultatif
- units : facultatif
- zunits : à utiliser uniquement si “elevation” est renseigné : est donc facultatif sinon interdit.
- projection : facultatif

**Les règles à suivre** :

- east doit être compris entre [-180 à 180] et contenir des valeurs numériques en degrés décimaux
- north doit être compris entre [-90 à +90] et contenir des valeurs numériques en degrés décimaux
- elevation doit être compris entre [-6 371 000 et 8 849]
- units : la seule valeur acceptée par défaut est “signed decimal degrees”
- zunits : la seule valeur acceptée est “metres”
- projection : la seule valeur acceptée est “WGS84”

Des exemples de syntaxes :

- east=43.244591; north=-11.699912; name=Moroni
- east=27; north=46.5;name=Moldova
- east=-2.83333; north=48.16667;name=Bretagne

Un exemple d’utilisation de l’encodage `dcterms:Point` associé à `dcterms:spatial` : https://nakala.fr/10.34847/nkl.62da51u0.

### Encodage `dcterms:URI` (lien web)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsuri-lien-web)

L’encodage `dcterms:URI` peut être associé à pratiquement toutes les propriétés du Dublin Core **tant que l’information saisie est uniquement un lien web**.

`dcterms:URI` sert à encoder les liens web (URI) selon la spécification du IETF - *Internet Engineering Task Force* :

< [The set of identifiers constructed according to the generic syntax for Uniform Resource Identifiers as specified by the Internet Engineering Task Force](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/URI).

Pour utiliser cet encodage dans NAKALA, sélectionner la propriété de votre choix (zone “Ajouter d’autres métadonnées”), puis dans le champ `Type`, sélectionner `dcterms:URI` à la condition que la métadonnée contienne uniquement un lien web qui pointe vers une ressource. Ne rien renseigner dans le champ `Pas d'information de langue`.

Un exemple d’utilisation de l’encodage `dcterms:URI` associé à une des sous-propriétés de `dcterms:relation` : https://nakala.fr/10.34847/nkl.49b2d984.

Un exemple où la propriété `dcterms:relation` est renseignée avec une URI sans l’encodage `dcterms:URI` - on note que le lien n’est pas cliquable à la différence de l’exemple précédent : https://nakala.fr/10.34847/nkl.d0b573b0

### Encodage `dcterms:W3CDTF` (format de date)[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#encodage-dctermsw3cdtf-format-de-date)

L’encodage `dcterms:W3CDTF` peut être associé aux propriétés `dcterms:date` et à ses sous-propriétés ; `dcterms:temporal` ; `dcterms:coverage` ; `dcterms:subject`.

`dcterms:W3CDTF` sert à encoder les formats de dates selon les spécifications du W3C – *World Wide Web Consortium* :

< [The set of dates and times constructed according to the W3C Date and Time Formats Specification](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/W3CDTF).

Pour utiliser cet encodage dans NAKALA, sélectionner les propriétés : `dcterms:date` ou une de ses sous-propriétés (zone “Ajouter d’autres métadonnées”) ; `dcterms:temporal` ; `dcterms:coverage` ; `dcterms:subject`, puis dans le champ `Type`, sélectionner `dcterms:W3CDTF`. Ne rien renseigner dans le champ `Pas d'information de langue`.

**Les règles à suivre** :

- les années doivent comporter au moins 4 chiffres. Par exemple : 0030 ; 1986 ; 30000
- les années peuvent être négatives : -0330; -0030
- le format peut être :
    - YYYY-MM-DD (année-mois-jour). Exemple : 2024-03-02
    - YYYY-MM (année-mois). Exemple : 2024-03
    - YYYY (année). Exemple : 2024
    - 1999-09-25T14:20+10:00

Des exemples de formats acceptés :

- 0330
- 300000
- 1939
- 1999-09-25T16:40+10:00

Un exemple d’utilisation de l’encodage `dcterms:W3CDTF` associé à une sous-propriété de `dcterms:date` : https://nakala.fr/10.34847/nkl.c00e3449.

## Publication des métadonnées après attribution du DOI[¶](https://documentation.huma-num.fr/nakala-guide-de-description/#publication-des-metadonnees-apres-attribution-du-doi)

Dans NAKALA, les métadonnées sont sous licence CC-BY afin de faciliter leur exposition (interopérabilité, moissonnage, référencement).

Chaque donnée publiée dans NAKALA se voit attribuer un Digital Object Identifier (DOI Datacite), un identifiant pérenne permettant la citation à long terme de la donnée. Cette attribution fait l’objet de l’enregistrement de métadonnées, et au titre de la pérennité des citations, ces informations ont vocation à être disponibles à long terme.

Ainsi une donnée au statut ‘Public’ dans NAKALA est exposée par le serveur OAI-PMH de NAKALA et publiée dans [Datacite](https://datacite.org/).

Chaque collection dans NAKALA est un SET dans l’entrepôt OAI-PMH de NAKALA : https://api.nakala.fr/oai2.

Il est donc important d’avoir des descriptions aussi claires et précises que possible des données qui sont déposées dans NAKALA.

- Un outil pour formater, à partir du DOI de la donnée, une citation de NAKALA dans d’autres normes bibliographiques : [DOI Citation Formatter](https://citation.crosscite.org/).
- Un outil de recherche dans les métadonnées exposées dans DataCite : [Datacite metadata search](https://search.datacite.org/). Les métadonnées sont récupérables dans cette interface dans les formats de DataCite (XML ou JSON) et de Schema.org (JSON-LD).

CC BY-NC-SA 4.0

Générée avec [MkDocs](https://www.mkdocs.org/) avec un [thème](https://github.com/readthedocs/sphinx_rtd_theme) fourni par [Read the Docs](https://readthedocs.org/).