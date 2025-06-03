import csv
import os
import json
from typing import Dict, Any, List
import requests
from datetime import datetime
import openapi_client
from openapi_client.rest import ApiException

# Configuration
api_url = "https://apitest.nakala.fr"
api_key = 'aae99aba-476e-4ff2-2886-0aaf1bfa6fd2'
configuration = openapi_client.Configuration(host=api_url)
configuration.api_key['apiKey'] = api_key

# Output file setup
output = open('output.csv', 'w')
outputWriter = csv.writer(output)
header = ['identifier', 'files', 'title', 'status', 'response']
outputWriter.writerow(header)

# Initialize API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create API instances
    datas_api = openapi_client.DatasApi(api_client)
    
    # Read the dataset
    with open('simple-dataset/dataset.csv', newline='') as f:
        reader = csv.reader(f)
        dataset = list(reader)
    dataset.pop(0)  # Remove header row

    # Process each row
    for num, data in enumerate(dataset):
        filenames = data[0].split(';')
        status = data[1]
        datatype = data[2]
        title = data[3]
        authors = data[4].split(';')
        date = data[5]
        license = data[6]
        description = data[7]
        keywords = data[8].split(';')
        datarights = data[9].split(';')

        outputData = ['', '', title, '', '']

        print('CREATION DE LA DONNEE ' + str(num) + " : " + title)

        nakala_files: List[Dict[str, Any]] = []
        outputFiles = []

        # Upload files
        try:
            for filename in filenames:
                print('Envoi du fichier ' + filename + '...')
                file_path = os.path.join('./simple-dataset/img/', filename)
                
                # Upload the file using requests
                try:
                    # Prepare multipart form data exactly as in original script
                    payload: Dict[str, Any] = {}
                    files = [
                        (
                            'file',
                            (
                                filename,
                                open(file_path, 'rb'),
                                'image/jpeg'
                            )
                        )
                    ]
                    headers = {'X-API-KEY': api_key}
                    
                    # Make the request
                    response = requests.request(
                        'POST',
                        f"{api_url}/datas/uploads",
                        headers=headers,
                        data=payload,
                        files=files
                    )
                    
                    if response.status_code == 201:
                        file_info = response.json()
                        # Add embargo date
                        file_info['embargoed'] = (
                            datetime.now().strftime("%Y-%m-%d")
                        )
                        nakala_files.append(file_info)
                        # Add to output files
                        file_str = f"{filename},{file_info['sha1']}"
                        outputFiles.append(file_str)
                    else:
                        raise ApiException(
                            status=response.status_code,
                            reason=response.text
                        )
                        
                except Exception as e:
                    print(f"Error uploading file {filename}: {e}")
                    outputFiles.append(filename)
                    outputData[1] = ';'.join(outputFiles)
                    outputData[3] = 'ERROR'
                    outputData[4] = str(e)
                    outputWriter.writerow(outputData)
                    raise

            # Update output with file info
            outputData[1] = ';'.join(outputFiles)
            
            # Prepare metadata
            metas = []
            
            # Type metadata
            metas.append({
                "value": datatype,
                "typeUri": "http://www.w3.org/2001/XMLSchema#anyURI",
                "propertyUri": "http://nakala.fr/terms#type"
            })
            
            # Title metadata
            metas.append({
                "value": title,
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#title"
            })
            
            # Authors metadata
            for author in authors:
                surname_givenname = author.split(',')
                if len(surname_givenname) == 2:
                    # Keep author data as an object, not a JSON string
                    author_data = {
                        "givenname": surname_givenname[1].strip(),
                        "surname": surname_givenname[0].strip()
                    }
                    metas.append({
                        "value": [author_data],  # Wrap in array as required
                        "propertyUri": "http://nakala.fr/terms#creator"
                    })
            
            # Date metadata
            metas.append({
                "value": date,
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#created"
            })
            
            # License metadata
            metas.append({
                "value": license,
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://nakala.fr/terms#license"
            })
            
            # Description metadata
            metas.append({
                "value": description,
                "lang": "fr",
                "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                "propertyUri": "http://purl.org/dc/terms/description"
            })
            
            # Keywords metadata
            for keyword in keywords:
                if keyword:  # Only add non-empty keywords
                    metas.append({
                        "value": keyword,
                        "lang": "fr",
                        "typeUri": "http://www.w3.org/2001/XMLSchema#string",
                        "propertyUri": "http://purl.org/dc/terms/subject"
                    })
            
            # Prepare rights - only include valid group IDs
            rights = []
            # Known valid group IDs
            valid_group_ids = [
                'de0f2a9b-a198-48a4-8074-db5120187a16'
            ]
            for dataright in datarights:
                if dataright:  # Only process non-empty rights
                    right_parts = dataright.split(',')
                    if len(right_parts) == 2:
                        group_id = right_parts[0].strip()
                        # Only add if group ID is in valid list
                        if group_id in valid_group_ids:
                            rights.append({
                                "id": group_id,
                                "role": right_parts[1].strip()
                            })
            
            # Create data payload
            data_payload = {
                "status": status,
                "files": nakala_files,
                "metas": metas,
                "rights": rights
            }
            
            try:
                # Convert payload to JSON string
                payload_str = json.dumps(data_payload)
                headers = {
                    'Content-Type': 'application/json',
                    'X-API-KEY': api_key
                }
                # Create the data entry using requests
                response = requests.request(
                    'POST',
                    f"{api_url}/datas",
                    headers=headers,
                    data=payload_str
                )
                
                if response.status_code == 201:
                    result = response.json()
                    print(
                        f'La donnée {num} a bien été créée : '
                        f'{result["payload"]["id"]}\n'
                    )
                    outputData[0] = result["payload"]["id"]
                    outputData[3] = 'OK'
                    outputData[4] = response.text
                else:
                    raise ApiException(
                        status=response.status_code,
                        reason=response.text
                    )
                    
            except Exception as e:
                print(f"Error creating data: {e}")
                outputData[3] = 'ERROR'
                outputData[4] = str(e)
                
        except Exception as e:
            # Only update if not already marked as error
            if outputData[3] != 'ERROR':
                print(f"Error processing entry: {e}")
                outputData[3] = 'ERROR'
                outputData[4] = str(e)
        
        outputWriter.writerow(outputData)

# Close the output file
output.close()
