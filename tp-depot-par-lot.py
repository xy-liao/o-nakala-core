import csv, requests, json, time

# Endpoint API & Clef d'API
apiUrl = 'https://apitest.nakala.fr'
apiKey = 'aae99aba-476e-4ff2-2886-0aaf1bfa6fd2'

# 1.1 Lecture du fichier CSV
with open('simple-dataset/dataset.csv', newline='') as f:
    reader = csv.reader(f)
    dataset = list(reader)
dataset.pop(0) # suppression des titres des colonnes

# 1.2 Préparation d'un fichier de sortie
output = open('output.csv', 'w') # ouverture d'un fichier en mode écriture
outputWriter = csv.writer(output) # création d'un objet pour écrire dans ce fichier
header = ['identifier', 'files', 'title', 'status', 'response'] # nom des colonnes à insérer dans ce fichier
outputWriter.writerow(header) # écriture du nom des colonnes dans ce fichier

# 2. Parcours des différentes lignes du fichier
for num, data in enumerate(dataset):
    
    # 2.1. Récupération des infos disponibles sur la donnée à créer
    filenames = data[0].split(';') # on distingue bien les valeurs séparées par des points-virgules
    status = data[1]
    datatype = data[2]
    title = data[3]
    authors = data[4].split(';')
    date = data[5]
    license = data[6]
    description = data[7]
    keywords = data[8].split(';')
    datarights = data[9].split(';')
    
    outputData = ['','',title,'','']; # variable où seront stockées les informations à écrire dans le fichier de sortie
    
    print('CREATION DE LA DONNEE ' + str(num) + " : " + title)
    
    # 2.2. Envoi des fichiers à l'API
    files = [] # variable pour stocker les informations retournées en JSON par l'API à chaque upload.
    outputFiles = [] # variable pour stocker les informations à écrire dans le fichier de sortie concernant les fichiers uploadés
    for filename in filenames: # on parcours l'ensemble des fichiers d'une donnée
        goToNextData = False # variable pour savoir s'il faut passer à la donnée suivante en cas d'erreur lors d'un upload
        print('Envoi du fichier ' + filename + '...') # on affiche un message pour le suivi de l'upload
        # écriture de la requête à l'API (ne contient pas de body en JSON, mais un fichier et un clef d'API)
        payload={}
        postfiles=[('file',(filename,open('./simple-dataset/img/' + filename, 'rb'),'image/jpeg'))]
        headers = {'X-API-KEY': apiKey }
        # appel à l'API pour uploader le fichier
        response = requests.request('POST', apiUrl + '/datas/uploads', headers=headers, data=payload, files=postfiles)
        # si l'upload s'est bien passé, on stocke les informations retournés par l'API dans la variable 'files'
        if ( 201 == response.status_code ):
            # avant de stocker les informations retournées par l'API sur le fichier, on y ajoute une date d'embargo
            file = json.loads(response.text)
            file["embargoed"] = time.strftime("%Y-%m-%d") # on renseigne la date du jour
            files.append(file)
            # ajout du nom du fichier et du sha1 aux informations à écrire dans le fichier de sortie
            outputFiles.append(filename + ',' + file["sha1"])
        else:
            # une erreur s'est produite avec un upload
            outputFiles.append(filename) # on ajoute le nom du fichier aux informations à écrire dans le fichier de sortie
            outputData[1] = ';'.join(outputFiles)
            outputData[3] = 'ERROR' # on complète les informations à écrire dans le fichier de sortie en indiquant qu'il y a eu une erreur
            outputData[4] = response.text # on insère ici le retour de l'API
            outputWriter.writerow(outputData) # on écrit dans le fichier de sortie
            print ("Certains fichiers n'ont pas pu être envoyés, on passe à la donnée suivante...") # on affiche un message d'erreur
            goToNextData = True # on indique dans cette variable qu'il faut passer à la donnée suivante
            break # on stop l'upload des autres fichiers de la donnée
    if goToNextData: continue # on passe à la donnée suivante s'il y a eu une erreur
    
    # 2.3. On garde une trace pour le fichier de sortie de la liste des fichiers uploadés
    outputData[1] = ';'.join(outputFiles)
    
    # 2.4. Reconstruction des métadonnées
    metas = [] # on stocke dans cette variable l'ensemble des métadonnées dans le format attendu
    
    # la métadonnée type (obligatoire)
    metaType = {
        "value": datatype, # on insère ici le contenu de la colonne "datatype" (un seul type par donnnée)
        "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI", # on indique ici que la valeur renseignée est de type URI
        "propertyUri": "http://nakala.fr/terms#type" # on indique ici le champ "type" issu du vocabulaire NAKALA
    }
    metas.append(metaType) # ajout de la métadonnée dans le tableau "metas"
    
    # la métadonnée titre (obligatoire)
    metaTitle = {
        "value": title, # on insère ici le contenu de la colonne "title" (un seul titre par donnnée)
        "lang": "fr", # on indique ici la langue du titre (cf. ISO-639-1 ou ISO-639-3 pour les langues moins courantes)
        "typeUri": "http://www.w3.org/2001/XMLSchema#string", # on indique ici que la valeur renseignée est une chaîne de caractères
        "propertyUri": "http://nakala.fr/terms#title" # on indique ici le champ "title" issu du vocabulaire de NAKALA
    }
    metas.append(metaTitle)
    
    # les métadonnées auteurs (obligatoire pour une donnée publiée)
    for author in authors: # la colonne "authors" peut comporter plusieurs valeurs qu'on parcours une à une
        # pour chaque valeur, on sépare le nom et le prénom pour construire la métadonnée nakala:creator
        surnameGivenname = author.split(',')
        metaAuthor = {
            "value": { # la valeur de cette métadonnée n'est pas une simple chaîne de caractères, mais un objet composé d'au minimum deux propriétées (givenname et surname)
                "givenname": surnameGivenname[1], # on insère ici le prénom
                "surname": surnameGivenname[0] # on insère ici le nom de famille
            },
            "propertyUri": "http://nakala.fr/terms#creator" # on indique ici le champ "creator" issu du vocabulaire de NAKALA
        }
        metas.append(metaAuthor)
        
    # la métadonnée date de création (obligatoire pour une donnée publiée)
    metaCreated = {
        "value": date, # on insère ici le contenu de la colonne "date" (une seule date de création par donnée)
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://nakala.fr/terms#created"
    }
    metas.append(metaCreated)
    
    # la métadonnée licence (obligatoire pour une donnée publiée)
    metaLicense = {
        "value": license, # On insère ici le contenu de la colonne "license" (une seule license par donnée)
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://nakala.fr/terms#license"
    }
    metas.append(metaLicense)
    
    # la métadonnée description (facultative)
    metaDescription = {
        "value": description, # on insère ici le contenu de la colonne "description" (une seule description par donnée)
        "lang": "fr",
        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
        "propertyUri": "http://purl.org/dc/terms/description" # notez qu'il ne s'agit plus ici d'une propriété issue du vocabulaire NAKALA, mais du vocabulaire Dcterms
    }
    metas.append(metaDescription)
    
    # les métadonnées mots-clés (facultatives)
    for keyword in keywords: # on parcours les valeurs de la colonne "keywords"
        metaKeyword = {
            "value": keyword, # on insère ici la valeur d'un mot-clé
            "lang": "fr",
            "typeUri": "http://www.w3.org/2001/XMLSchema#string",
            "propertyUri": "http://purl.org/dc/terms/subject" # notez qu'il ne s'agit plus ici d'une propriété issue du vocabulaire NAKALA, mais du vocabulaire Dcterms
        }
        metas.append(metaKeyword)
    
    # 2.5. Reconstruction des droits
    rights = [] # on stocke les droits d'une donnée dans un tableau
    for dataright in datarights: # on parcours les valeurs de la colonne "rights"
        datarightSplit = dataright.split(',') # chaque valeur est composée d'un id et d'un rôle séparé par une virgule. On sépare ces valeurs
        if len(datarightSplit) == 2: # on vérifie qu'on a bien deux valeurs uniquement
            right = { # on reconstruit l'objet "right" composé des propriétés "id" et "role"
                "id": datarightSplit[0],
                "role": datarightSplit[1]
            }
            rights.append(right) # on ajout l'objet "right" dans le tableau "rights"
    
    # 3. Envoi de la donnée à NAKALA
    postdata = { # variable contenant le contenu de la requête
        "status" : status,
        "files" : files,
        "metas" : metas,
        "rights": rights
    }
    content = json.dumps(postdata) # serialisation du contenu en JSON
    headers = { # header de la requête
      'Content-Type': 'application/json',
      'X-API-KEY': apiKey,
    }
    response = requests.request('POST', apiUrl + '/datas', headers=headers, data=content) # requête à l'API
    if ( 201 == response.status_code ): # on obtient un code 201 si tout s'est bien passé
        parsed = json.loads(response.text) # on parse la réponse de l'API
        print('La donnée ' + str(num) + ' a bien été créée : ' + parsed["payload"]["id"] + '\n') # affichage d'un message de succès
        outputData[0] = parsed["payload"]["id"] # on stocke les informations nécessaire pour le fichier de sortie
        outputData[3] = 'OK'
        outputData[4] = response.text
    else:
        print("Une erreur s'est produite !") # en cas d'erreur, on affiche un message
        outputData[3] = 'ERROR' # on complète les informations nécessaires pour le fichier de sortie
        outputData[4] = response.text
    outputWriter.writerow(outputData) # on écrit les informations dans le fichier de sortie

# 4. Fermeture du fichier de sortie
output.close()