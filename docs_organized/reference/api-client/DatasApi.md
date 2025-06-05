# openapi_client.DatasApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**data_identifier_file_identifier_get**](DatasApi.md#data_identifier_file_identifier_get) | **GET** /data/{identifier}/{fileIdentifier} | Téléchargement du fichier \&quot;fileIdentifier\&quot; de la donnée \&quot;identifier\&quot;.
[**datas_identifier_citation_get**](DatasApi.md#datas_identifier_citation_get) | **GET** /datas/{identifier}/citation | Citation de la donnée.
[**datas_identifier_collections_delete**](DatasApi.md#datas_identifier_collections_delete) | **DELETE** /datas/{identifier}/collections | Suppression d&#39;une donnée d&#39;un ensemble de collections.
[**datas_identifier_collections_get**](DatasApi.md#datas_identifier_collections_get) | **GET** /datas/{identifier}/collections | Récupération de la liste des collections contenant la donnée.
[**datas_identifier_collections_post**](DatasApi.md#datas_identifier_collections_post) | **POST** /datas/{identifier}/collections | Ajout d&#39;une donnée dans un ensemble de collections.
[**datas_identifier_collections_put**](DatasApi.md#datas_identifier_collections_put) | **PUT** /datas/{identifier}/collections | Remplacement de l&#39;ensemble des collections d&#39;une donnée.
[**datas_identifier_delete**](DatasApi.md#datas_identifier_delete) | **DELETE** /datas/{identifier} | Suppression d&#39;une donnée.
[**datas_identifier_files_file_identifier_delete**](DatasApi.md#datas_identifier_files_file_identifier_delete) | **DELETE** /datas/{identifier}/files/{fileIdentifier} | Suppression de fichier à une donnée.
[**datas_identifier_files_get**](DatasApi.md#datas_identifier_files_get) | **GET** /datas/{identifier}/files | Récupération des métadonnées des fichiers associés à une donnée.
[**datas_identifier_files_post**](DatasApi.md#datas_identifier_files_post) | **POST** /datas/{identifier}/files | Ajout d&#39;un fichier à une donnée.
[**datas_identifier_get**](DatasApi.md#datas_identifier_get) | **GET** /datas/{identifier} | Récupération des informations sur une donnée.
[**datas_identifier_metadatas_delete**](DatasApi.md#datas_identifier_metadatas_delete) | **DELETE** /datas/{identifier}/metadatas | Suppression de métadonnées pour une donnée.
[**datas_identifier_metadatas_get**](DatasApi.md#datas_identifier_metadatas_get) | **GET** /datas/{identifier}/metadatas | Récupération de la liste des métadonnées d&#39;une donnée.
[**datas_identifier_metadatas_post**](DatasApi.md#datas_identifier_metadatas_post) | **POST** /datas/{identifier}/metadatas | Ajout d&#39;une nouvelle métadonnée à une donnée.
[**datas_identifier_put**](DatasApi.md#datas_identifier_put) | **PUT** /datas/{identifier} | Modification des informations d&#39;une donnée.
[**datas_identifier_relations_delete**](DatasApi.md#datas_identifier_relations_delete) | **DELETE** /datas/{identifier}/relations | Suppression des relations sur une donnée.
[**datas_identifier_relations_get**](DatasApi.md#datas_identifier_relations_get) | **GET** /datas/{identifier}/relations | Récupération de la liste des relations d&#39;une donnée.
[**datas_identifier_relations_patch**](DatasApi.md#datas_identifier_relations_patch) | **PATCH** /datas/{identifier}/relations | Modification du commentaire d&#39;une relation.
[**datas_identifier_relations_post**](DatasApi.md#datas_identifier_relations_post) | **POST** /datas/{identifier}/relations | Ajout de relations sur une donnée.
[**datas_identifier_rights_delete**](DatasApi.md#datas_identifier_rights_delete) | **DELETE** /datas/{identifier}/rights | Suppression des droits pour un utilisateur ou un groupe d&#39;utilisateurs sur une donnée.
[**datas_identifier_rights_get**](DatasApi.md#datas_identifier_rights_get) | **GET** /datas/{identifier}/rights | Récupération des groupes et des utilisateurs ayant des droits sur la donnée.
[**datas_identifier_rights_post**](DatasApi.md#datas_identifier_rights_post) | **POST** /datas/{identifier}/rights | Ajout de droits sur une donnée.
[**datas_identifier_status_get**](DatasApi.md#datas_identifier_status_get) | **GET** /datas/{identifier}/status | Récupération du statut d&#39;une donnée.
[**datas_identifier_status_status_put**](DatasApi.md#datas_identifier_status_status_put) | **PUT** /datas/{identifier}/status/{status} | Changement du statut d&#39;une donnée.
[**datas_identifier_versions_get**](DatasApi.md#datas_identifier_versions_get) | **GET** /datas/{identifier}/versions | Récupération de la liste des versions d&#39;une donnée.
[**datas_post**](DatasApi.md#datas_post) | **POST** /datas | Dépôt d&#39;une nouvelle donnée.
[**datas_uploads_file_identifier_delete**](DatasApi.md#datas_uploads_file_identifier_delete) | **DELETE** /datas/uploads/{fileIdentifier} | Suppression d&#39;un fichier déposé dans l&#39;espace temporaire
[**datas_uploads_get**](DatasApi.md#datas_uploads_get) | **GET** /datas/uploads | Récupération pour un utilisateur de la liste des objets fichiers déposés non encore associés à une donnée.
[**datas_uploads_post**](DatasApi.md#datas_uploads_post) | **POST** /datas/uploads | Dépôt de fichier.
[**embed_identifier_file_identifier_get**](DatasApi.md#embed_identifier_file_identifier_get) | **GET** /embed/{identifier}/{fileIdentifier} | Visionneuse NAKALA du fichier \&quot;fileIdentifier\&quot; de la donnée \&quot;identifier\&quot;.
[**iiif_identifier_file_identifier_info_json_get**](DatasApi.md#iiif_identifier_file_identifier_info_json_get) | **GET** /iiif/{identifier}/{fileIdentifier}/info.json | IIIF Image API - Information sur l&#39;image \&quot;fileIdentifier\&quot; de la donnée \&quot;identifier\&quot;.
[**iiif_identifier_file_identifier_region_size_rotation_quality_format_get**](DatasApi.md#iiif_identifier_file_identifier_region_size_rotation_quality_format_get) | **GET** /iiif/{identifier}/{fileIdentifier}/{region}/{size}/{rotation}/{quality}.{format} | IIIF Image API - Transformation de l&#39;image \&quot;fileIdentifier\&quot; de la donnée \&quot;identifier\&quot;.


# **data_identifier_file_identifier_get**
> data_identifier_file_identifier_get(identifier, file_identifier, content_disposition=content_disposition)

Téléchargement du fichier \"fileIdentifier\" de la donnée \"identifier\".

Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    file_identifier = 'file_identifier_example' # str | Identifiant du fichier
    content_disposition = inline # str | Entête HTTP Content-Disposition. inline : affichage du fichier dans le navigateur ou attachment : le fichier doit être téléchargé (optional) (default to inline)

    try:
        # Téléchargement du fichier \"fileIdentifier\" de la donnée \"identifier\".
        api_instance.data_identifier_file_identifier_get(identifier, file_identifier, content_disposition=content_disposition)
    except Exception as e:
        print("Exception when calling DatasApi->data_identifier_file_identifier_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **file_identifier** | **str**| Identifiant du fichier | 
 **content_disposition** | **str**| Entête HTTP Content-Disposition. inline : affichage du fichier dans le navigateur ou attachment : le fichier doit être téléchargé | [optional] [default to inline]

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Le contenu du fichier |  -  |
**401** | Donnée non publiée, clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas ou n&#39;est pas accessible |  -  |
**500** | Erreur interne |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_citation_get**
> str datas_identifier_citation_get(identifier, style=style, locale=locale)

Citation de la donnée.

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    style = 'apa' # str | Style parmi la liste dans https://github.com/citation-style-language/styles (optional) (default to 'apa')
    locale = 'en-US' # str | Langue parmi la liste dans https://github.com/citation-style-language/locales (optional) (default to 'en-US')

    try:
        # Citation de la donnée.
        api_response = api_instance.datas_identifier_citation_get(identifier, style=style, locale=locale)
        print("The response of DatasApi->datas_identifier_citation_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_citation_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **style** | **str**| Style parmi la liste dans https://github.com/citation-style-language/styles | [optional] [default to &#39;apa&#39;]
 **locale** | **str**| Langue parmi la liste dans https://github.com/citation-style-language/locales | [optional] [default to &#39;en-US&#39;]

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain, application/json, text/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retourne la citation demandée |  -  |
**403** | La donnée n&#39;est pas publique ou n&#39;a pas de DOI valide ou bien l&#39;environnement dans lequel vous êtes ne permet pas la citation |  -  |
**404** | La donnée n&#39;existe pas ou n&#39;a pas de DOI valide |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_collections_delete**
> datas_identifier_collections_delete(identifier, collections)

Suppression d'une donnée d'un ensemble de collections.

L'utilisateur doit au minimum avoir les droits de lecture sur la donnée et être éditeur des différentes collections.
Ni la donnée, ni les collections ne sont supprimées de NAKALA.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    collections = ['collections_example'] # List[str] | Liste des identifiants des collections d'où la donnée doit être supprimée

    try:
        # Suppression d'une donnée d'un ensemble de collections.
        api_instance.datas_identifier_collections_delete(identifier, collections)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_collections_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **collections** | [**List[str]**](str.md)| Liste des identifiants des collections d&#39;où la donnée doit être supprimée | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | La donnée a été supprimé des collections |  -  |
**401** | Clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droits insuffisants pour supprimer la donnée des collections |  -  |
**404** | Collection ou donnée non trouvée |  -  |
**500** | Erreur lors de la suppression de la donnée des collections |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_collections_get**
> List[Collection2] datas_identifier_collections_get(identifier, order=order)

Récupération de la liste des collections contenant la donnée.

Retourne la liste des collections contenant la donnée et sur lesquelles l'utilisateur courant a les droits de lecture.

Il est possible de trier les collections en fonction de leur date de création (`creDate,asc` ou `creDate,desc`) ou de leur titre (`title,asc` ou `title,desc`)
Lorsque les collections sont triées en fonction de leur titre, c'est le premier titre disponible dans la langue de l'en-tête `Accept-Language` qui est pris en compte.
Si aucun en-tête `Accept-Language` n'est renseigné, l'anglais est la langue par défaut. Si aucun titre ne correspond à la langue du header, c'est le premier titre de la collection qui est pris par défaut.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.collection2 import Collection2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    order = 'creDate,desc' # str | Tri sur les collections (optional) (default to 'creDate,desc')

    try:
        # Récupération de la liste des collections contenant la donnée.
        api_response = api_instance.datas_identifier_collections_get(identifier, order=order)
        print("The response of DatasApi->datas_identifier_collections_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_collections_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **order** | **str**| Tri sur les collections | [optional] [default to &#39;creDate,desc&#39;]

### Return type

[**List[Collection2]**](Collection2.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | La liste des collections |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_collections_post**
> datas_identifier_collections_post(identifier, collections)

Ajout d'une donnée dans un ensemble de collections.

L'utilisateur doit au minimum avoir les droits de lecture sur la donnée et être éditeur des différentes collections
Une collection publique ne peut contenir que des données publiées.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    collections = ['collections_example'] # List[str] | Liste des identifiants des collections à associer à la donnée

    try:
        # Ajout d'une donnée dans un ensemble de collections.
        api_instance.datas_identifier_collections_post(identifier, collections)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_collections_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **collections** | [**List[str]**](str.md)| Liste des identifiants des collections à associer à la donnée | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | La donnée a été ajoutée dans les collections |  -  |
**401** | Clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droits insuffisants pour ajouter la donnée dans les collections |  -  |
**404** | Collection ou donnée non trouvée |  -  |
**500** | Erreur lors de l&#39;ajout de la donnée dans les collections |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_collections_put**
> datas_identifier_collections_put(identifier, collections)

Remplacement de l'ensemble des collections d'une donnée.

Seules les collections dont vous êtes au moins éditeur seront prises en compte. Les autres resteront inchangées.
L'utilisateur doit au minimum avoir les droits de lecture sur la donnée et être éditeur des différentes collections
Une collection publique ne peut contenir que des données publiées.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    collections = ['collections_example'] # List[str] | Liste exhaustive des identifiants des collections (dont vous êtes éditeur) à associer à la donnée

    try:
        # Remplacement de l'ensemble des collections d'une donnée.
        api_instance.datas_identifier_collections_put(identifier, collections)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_collections_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **collections** | [**List[str]**](str.md)| Liste exhaustive des identifiants des collections (dont vous êtes éditeur) à associer à la donnée | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | La donnée est dans les collections soumises |  -  |
**401** | Clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droits insuffisants pour ajouter la donnée dans les collections |  -  |
**404** | Collection ou donnée non trouvée |  -  |
**500** | Erreur lors de l&#39;ajout de la donnée dans les collections |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_delete**
> datas_identifier_delete(identifier)

Suppression d'une donnée.

La suppression d'une donnée est autorisée uniquement si la donnée n'est pas publiée

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée

    try:
        # Suppression d'une donnée.
        api_instance.datas_identifier_delete(identifier)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Donnée supprimée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_files_file_identifier_delete**
> datas_identifier_files_file_identifier_delete(identifier, file_identifier)

Suppression de fichier à une donnée.

La suppression d'un fichier ne peut se faire que sur une donnée non publiée

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    file_identifier = 'file_identifier_example' # str | Identifiant du fichier

    try:
        # Suppression de fichier à une donnée.
        api_instance.datas_identifier_files_file_identifier_delete(identifier, file_identifier)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_files_file_identifier_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **file_identifier** | **str**| Identifiant du fichier | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Fichier supprimé de la donnée |  -  |
**401** | Donnée non publiée, clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas ou n&#39;est pas accessible |  -  |
**500** | La donnée n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_files_get**
> List[File2] datas_identifier_files_get(identifier)

Récupération des métadonnées des fichiers associés à une donnée.

Permet d'obtenir l'ensemble des informations sur les fichiers associés à une donnée. Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.file2 import File2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée

    try:
        # Récupération des métadonnées des fichiers associés à une donnée.
        api_response = api_instance.datas_identifier_files_get(identifier)
        print("The response of DatasApi->datas_identifier_files_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_files_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 

### Return type

[**List[File2]**](File2.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des métadonnées des fichiers |  -  |
**401** | Donnée non publiée, clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas ou n&#39;est pas accessible |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_files_post**
> datas_identifier_files_post(identifier, file=file)

Ajout d'un fichier à une donnée.

Permet d'ajouter un fichier à une donnée.

Attention, le fichier doit être déposé avant à l'aide de la requête POST /uploads

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.file import File
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    file = '/path/to/file' # File | Informations sur le fichier à ajouter (optional)

    try:
        # Ajout d'un fichier à une donnée.
        api_instance.datas_identifier_files_post(identifier, file=file)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_files_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **file** | [**File**](File.md)| Informations sur le fichier à ajouter | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Fichier ajouter |  -  |
**404** | La donnée n&#39;existe pas ou n&#39;est pas accessible |  -  |
**409** | La donnée contient déjà le fichier à ajouter |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_get**
> Data datas_identifier_get(identifier, metadata_format=metadata_format)

Récupération des informations sur une donnée.

Retourne l'ensemble des informations relatives à la donnée
- statut de la donnée
- liste des métadonnées
- liste des collections contenant la donnée
- métadonnées sur les fichiers associés à la donnée

Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.data import Data
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    metadata_format = 'metadata_format_example' # str | format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) (optional)

    try:
        # Récupération des informations sur une donnée.
        api_response = api_instance.datas_identifier_get(identifier, metadata_format=metadata_format)
        print("The response of DatasApi->datas_identifier_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **metadata_format** | **str**| format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) | [optional] 

### Return type

[**Data**](Data.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retourne l&#39;objet donnée |  -  |
**401** | Donnée non publiée, clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_metadatas_delete**
> datas_identifier_metadatas_delete(identifier, meta=meta)

Suppression de métadonnées pour une donnée.

Il est possible de passer un filtre dans le corps de la requête qui permettra de ne supprimer que certaines métadonnées
Par exemple pour supprimer les dcterms:subject en anglais il faudra passer l'objet suivant
```
{"lang": "en", "propertyUri": "http://purl.org/dc/terms/subject"}
```

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.meta2 import Meta2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    meta = openapi_client.Meta2() # Meta2 | Modèle de métadonnées à supprimer (optional)

    try:
        # Suppression de métadonnées pour une donnée.
        api_instance.datas_identifier_metadatas_delete(identifier, meta=meta)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_metadatas_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **meta** | [**Meta2**](Meta2.md)| Modèle de métadonnées à supprimer | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Nombre de métadonnées supprimées |  -  |
**401** | Clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droits insuffisants |  -  |
**404** | Aucune donnée trouvée à partir de l&#39;identifiant |  -  |
**500** | Erreur lors de la suppression de métadonnées |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_metadatas_get**
> List[Meta2] datas_identifier_metadatas_get(identifier, metadata_format=metadata_format)

Récupération de la liste des métadonnées d'une donnée.

une métadonnée contient
- une propriété
- une valeur (string ou objet auteur)
- un type (optionnel)
- un format (optionnel)

Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.meta2 import Meta2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    metadata_format = 'metadata_format_example' # str | format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) (optional)

    try:
        # Récupération de la liste des métadonnées d'une donnée.
        api_response = api_instance.datas_identifier_metadatas_get(identifier, metadata_format=metadata_format)
        print("The response of DatasApi->datas_identifier_metadatas_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_metadatas_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **metadata_format** | **str**| format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) | [optional] 

### Return type

[**List[Meta2]**](Meta2.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste de métadonnées |  -  |
**401** | Donnée privée, nécessite que l&#39;utilisateur dispose de droits sur la donnée |  -  |
**403** | Donnée privée, droits manquants sur la donnée |  -  |
**404** | Aucune donnée trouvée à partir de l&#39;identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_metadatas_post**
> datas_identifier_metadatas_post(identifier, meta=meta)

Ajout d'une nouvelle métadonnée à une donnée.

La métadonnée contient
- une propriété
- une valeur (string ou objet auteur)
- un type (optionnel)
- un format (optionnel)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.meta2 import Meta2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    meta = openapi_client.Meta2() # Meta2 | Métadonnée à ajouter (optional)

    try:
        # Ajout d'une nouvelle métadonnée à une donnée.
        api_instance.datas_identifier_metadatas_post(identifier, meta=meta)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_metadatas_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **meta** | [**Meta2**](Meta2.md)| Métadonnée à ajouter | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | La métadonnée a été ajoutée à la donnée |  -  |
**401** | Clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droits insuffisants pour modifier la donnée |  -  |
**404** | Aucune donnée trouvée à partir de l&#39;identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_put**
> datas_identifier_put(identifier, data=data)

Modification des informations d'une donnée.

Chaque entrée est facultative (rights, metas, files, status, collectionsIds, relations).
En revanche, chaque entrée doit contenir une liste exhaustive.
Par example, vous souhaitez ajouter un fichier : il faut renseigner l'ensemble des données précédentes en plus du fichier à ajouter.

Vous pouvez vider l'ensemble des données pour "rights", "collectionsIds" et "relations" en soumettant un tableau vide.

Note pour "files": vous devez uploader le fichier avant afin que l'API vous communique son SHA-1. Le nom du fichier est facultatif si vous ne souhaitez pas le modifier.

Note pour "collectionsIds" : seules les collections dont vous êtes au moins éditeur seront prises en compte. Les autres resteront inchangées.

Note pour "relations" : seules les relations créées depuis NAKALA seront prises en compte. Les relations créées automatiquement depuis d'autres entrepôts resteront inchangées.

L'édition des champs "metas" et "datas" requière le ROLE_EDITOR et l'édition des champs "status" et "rights" requière le ROLE_ADMIN.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.data2 import Data2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    data = openapi_client.Data2() # Data2 | Donnée à enregistrer (optional)

    try:
        # Modification des informations d'une donnée.
        api_instance.datas_identifier_put(identifier, data=data)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **data** | [**Data2**](Data2.md)| Donnée à enregistrer | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | La donnée a été modifiée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droits sur la donnée insuffisants |  -  |
**404** | La donnée n&#39;existe pas |  -  |
**500** | Erreur lors de l&#39;enregistrement de la nouvelle donnée |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_relations_delete**
> datas_identifier_relations_delete(identifier, relation=relation)

Suppression des relations sur une donnée.

Permet de supprimer une ou plusieurs relations entre la donnée avec d'autres données provenant de NAKALA ou d'autres entrepôts de données (ex: HAL).
Il est possible de passer un filtre dans le corps de la requête qui permettra de ne supprimer que certaines relations.
Par exemple pour supprimer toutes les relations vers les données provenant de l''entrepôt HAL :
```
{"repository": "hal"}
```

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.relation2 import Relation2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    relation = openapi_client.Relation2() # Relation2 | Relation à supprimer (optional)

    try:
        # Suppression des relations sur une donnée.
        api_instance.datas_identifier_relations_delete(identifier, relation=relation)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_relations_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **relation** | [**Relation2**](Relation2.md)| Relation à supprimer | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Relations supprimés |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |
**500** | Erreur lors de la suppression de la relation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_relations_get**
> List[Relation] datas_identifier_relations_get(identifier)

Récupération de la liste des relations d'une donnée.

Permet de retourner la liste des ressources externes liées à la donnée. Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.relation import Relation
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée

    try:
        # Récupération de la liste des relations d'une donnée.
        api_response = api_instance.datas_identifier_relations_get(identifier)
        print("The response of DatasApi->datas_identifier_relations_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_relations_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 

### Return type

[**List[Relation]**](Relation.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste de relations |  -  |
**401** | Donnée privée ou compte utilisateur inexistant |  -  |
**403** | Donnée privée, droits manquants sur la donnée |  -  |
**404** | Aucune donnée trouvée à partir de l&#39;identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_relations_patch**
> datas_identifier_relations_patch(identifier, relation=relation)

Modification du commentaire d'une relation.

Permet de modifier le commentaire d'une relation.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.relation2 import Relation2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    relation = openapi_client.Relation2() # Relation2 | Relation à modifier (optional)

    try:
        # Modification du commentaire d'une relation.
        api_instance.datas_identifier_relations_patch(identifier, relation=relation)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_relations_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **relation** | [**Relation2**](Relation2.md)| Relation à modifier | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Le commentaire a été modifié |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |
**409** | La relation envoyée correspond à plus d&#39;une relation |  -  |
**500** | Erreur du serveur |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_relations_post**
> datas_identifier_relations_post(identifier, relations=relations)

Ajout de relations sur une donnée.

Permet de lier une donnée avec d'autres données provenant de NAKALA ou d'autres entrepôts de données (ex: HAL).

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.relation2 import Relation2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    relations = [openapi_client.Relation2()] # List[Relation2] | tableau des nouvelles relations à ajouter à la donnée (optional)

    try:
        # Ajout de relations sur une donnée.
        api_instance.datas_identifier_relations_post(identifier, relations=relations)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_relations_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **relations** | [**List[Relation2]**](Relation2.md)| tableau des nouvelles relations à ajouter à la donnée | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Les relations ont bien été ajoutées à la donnée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |
**500** | Erreur lors de l&#39;ajout des relations sur la donnée |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_rights_delete**
> datas_identifier_rights_delete(identifier, right=right)

Suppression des droits pour un utilisateur ou un groupe d'utilisateurs sur une donnée.

La suppression des droits d'une donnée est autorisée aux utilisateurs ayant les droits propriétaire ou administrateur.
Il est possible de passer un filtre dans le corps de la requête qui permettra de ne supprimer que certains droits.
Par exemple pour supprimer tous les éditeurs d'une donnée :
```
{"role": "ROLE_EDITOR"}
```
Note: le droit **propriétaire** (ROLE_OWNER) d'une donnée ne peut pas être supprimé.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.delete_right import DeleteRight
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    right = openapi_client.DeleteRight() # DeleteRight | Droit à supprimer (optional)

    try:
        # Suppression des droits pour un utilisateur ou un groupe d'utilisateurs sur une donnée.
        api_instance.datas_identifier_rights_delete(identifier, right=right)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_rights_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **right** | [**DeleteRight**](DeleteRight.md)| Droit à supprimer | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Droits supprimés |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |
**500** | Erreur lors de la suppression du droit |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_rights_get**
> List[DetailedRight] datas_identifier_rights_get(identifier)

Récupération des groupes et des utilisateurs ayant des droits sur la donnée.

Permet de retourner une liste contenant
- l'utilisateur ou le groupe d'utilisateurs
- le droit sur la donnée
  - **propriétaire** (ROLE_OWNER) : consultation, modification, suppression, partage des droits de la donnée
  - **administrateur** (ROLE_ADMIN) : consultation, modification, suppression, partage des droits de la donnée
  - **modérateur** (ROLE_MODERATOR) : modération de la donnée
  - **éditeur** (ROLE_EDITOR) :  consultation, modification, suppression de la donnée
  - **lecteur** (ROLE_READER) :  consultation de la donnée même s'il n'est pas encore publiée
Note: Seule la personne ayant déposé la donnée peut avoir le droit **propriétaire**

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.detailed_right import DetailedRight
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée

    try:
        # Récupération des groupes et des utilisateurs ayant des droits sur la donnée.
        api_response = api_instance.datas_identifier_rights_get(identifier)
        print("The response of DatasApi->datas_identifier_rights_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_rights_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 

### Return type

[**List[DetailedRight]**](DetailedRight.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des utilisateurs et des groupes ayant des droits sur la donnée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_rights_post**
> datas_identifier_rights_post(identifier, rights=rights)

Ajout de droits sur une donnée.

Permet de rajouter des droits à un utilisateur ou un group d'utilisateurs sur une donnée.
Les droits possibles sont :
- **propriétaire** (ROLE_OWNER) : consultation, modification, suppression, partage des droits de la donnée, cession des droits à une liste d'utilisateurs
- **administrateur** (ROLE_ADMIN) : consultation, modification, suppression, partage des droits de la donnée
- **modérateur** (ROLE_MODERATOR) : modération de la donnée
- **éditeur** (ROLE_EDITOR) :  consultation, modification, suppression de la donnée
- **lecteur** (ROLE_READER) :  consultation de la donnée même si elle n'est pas encore publiée
Note: Le droit **propriétaire** (ROLE_OWNER) est attribué automatiquement au déposant de la donnée, mais peut être ré-attributé à une liste d'utilisateurs auquel le déposant appartient

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.post_right import PostRight
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    rights = [openapi_client.PostRight()] # List[PostRight] | tableau des nouveaux droits à ajouter à la donnée (optional)

    try:
        # Ajout de droits sur une donnée.
        api_instance.datas_identifier_rights_post(identifier, rights=rights)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_rights_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **rights** | [**List[PostRight]**](PostRight.md)| tableau des nouveaux droits à ajouter à la donnée | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Droits ajoutés sur la donnée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |
**500** | Erreur lors de l&#39;ajout du droit sur la donnée |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_status_get**
> datas_identifier_status_get(identifier)

Récupération du statut d'une donnée.

Retourne le statut de la donnée. Le statut peut être
- **pending** : donnée déposée mais pas encore en ligne
- **published** : donnée publiée
- **moderated** : donnée modérée
- **deleted** : donnée supprimée
- **old** : ancienne version d'une donnée publiée

Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée

    try:
        # Récupération du statut d'une donnée.
        api_instance.datas_identifier_status_get(identifier)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_status_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Statut de la donnée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_status_status_put**
> datas_identifier_status_status_put(identifier, status)

Changement du statut d'une donnée.

Permet de publier une donnée déposée (non encore publique) ou de modérer une donnée publiée.
Seuls les modérateurs peuvent modérer une donnée publiée.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    status = 'status_example' # str | Nouveau statut de la donnée

    try:
        # Changement du statut d'une donnée.
        api_instance.datas_identifier_status_status_put(identifier, status)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_status_status_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **status** | **str**| Nouveau statut de la donnée | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Status changé |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |
**500** | Erreur lors de l&#39;enregistrement du nouveau statut |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_identifier_versions_get**
> DatasIdentifierVersionsGet200Response datas_identifier_versions_get(identifier, version=version, limit=limit)

Récupération de la liste des versions d'une donnée.

Permet de retourner la liste des versions d'une donnée.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.datas_identifier_versions_get200_response import DatasIdentifierVersionsGet200Response
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    version = 'version_example' # str | Version de la donnée (optional)
    limit = '10' # str | Nombre de résultats par page (optional) (default to '10')

    try:
        # Récupération de la liste des versions d'une donnée.
        api_response = api_instance.datas_identifier_versions_get(identifier, version=version, limit=limit)
        print("The response of DatasApi->datas_identifier_versions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_identifier_versions_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **version** | **str**| Version de la donnée | [optional] 
 **limit** | **str**| Nombre de résultats par page | [optional] [default to &#39;10&#39;]

### Return type

[**DatasIdentifierVersionsGet200Response**](DatasIdentifierVersionsGet200Response.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des versions de la donnée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_post**
> datas_post(data=data)

Dépôt d'une nouvelle donnée.

Permet de déposer une donnée dans Nakala
Les fichiers associés à la donnée sont à déposer avant via POST /uploads

- Statut de la donnée (pending ou published)
- Liste des identifiants des collections où ranger la donnée. Une collection publique ne peut contenir que des données publiées.
- Métadonnées descriptives de la donnée :
lang : la liste des valeurs acceptées est disponible via GET /vocabularies/languages
typeUri : la liste des valeurs acceptées est disponible via GET /vocabularies/metadatatypes
propertyUri : la liste des valeurs acceptées est disponible via GET /vocabularies/properties
value : les valeurs de certaines métadonnées sont validées.
Par exemple http://nakala.fr/terms#license doit valider les codes retournés par GET /vocabularies/licenses et http://nakala.fr/terms#type ceux retournés par GET /vocabularies/datatypes
Les métadonnées http://nakala.fr/terms#type, http://nakala.fr/terms#title, http://nakala.fr/terms#creator, http://nakala.fr/terms#created et http://nakala.fr/terms#license sont obligatoires pour publier une donnée.
http://nakala.fr/terms#creator : renseignez un auteur sous la forme d'un objet {givenname, surname, orcid}. Indiquez null si l'auteur est anonyme
http://nakala.fr/terms#created : renseignez une date sous la forme année, année-mois ou année-mois-jour. Indiquez null si la date de création est inconnue
- Fichier(s) de la donnée :
name: le nom est facultatif si vous ne souhaitez pas le changer
sha1 : identifiant du fichier déposé via POST /datas/uploads
description : (optionnel) description sur le fichier
embargoed: (optionnel, format=Y-m-d) date de fin d'embargo
- Partage de droits sur cette donnée
- Relations : voir le schéma d'une relation sur le verbe POST /datas/{identifier}/relations

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.data2 import Data2
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    data = openapi_client.Data2() # Data2 | Informations sur la donnée à créer (optional)

    try:
        # Dépôt d'une nouvelle donnée.
        api_instance.datas_post(data=data)
    except Exception as e:
        print("Exception when calling DatasApi->datas_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data** | [**Data2**](Data2.md)| Informations sur la donnée à créer | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Enregistrement de la donnée |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**422** | La donnée ne contient pas les données obligatoires |  -  |
**500** | Erreur lors de l&#39;enregistrement de la donnée |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_uploads_file_identifier_delete**
> datas_uploads_file_identifier_delete(file_identifier)

Suppression d'un fichier déposé dans l'espace temporaire

Permet de supprimer un fichier présent dans l'espace temporaire

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    file_identifier = 'file_identifier_example' # str | 

    try:
        # Suppression d'un fichier déposé dans l'espace temporaire
        api_instance.datas_uploads_file_identifier_delete(file_identifier)
    except Exception as e:
        print("Exception when calling DatasApi->datas_uploads_file_identifier_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_identifier** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Le fichier a été supprimé |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Clé d&#39;API non valide ou utilisateur inconnu |  -  |
**404** | Le fichier n&#39;existe pas |  -  |
**500** | Erreur lors de la suppression du fichier |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_uploads_get**
> List[File3] datas_uploads_get()

Récupération pour un utilisateur de la liste des objets fichiers déposés non encore associés à une donnée.

Les fichiers déposés restent dans un espace temporaire le temps qu'ils soient associés à une donnée de Nakala ou soient automatiquement supprimés (toutes les 24 heures)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.file3 import File3
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)

    try:
        # Récupération pour un utilisateur de la liste des objets fichiers déposés non encore associés à une donnée.
        api_response = api_instance.datas_uploads_get()
        print("The response of DatasApi->datas_uploads_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_uploads_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[File3]**](File3.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des objets fichiers déposés |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Clé d&#39;API non valide ou utilisateur inconnu |  -  |
**500** | Erreur lors de la récupération des fichiers |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **datas_uploads_post**
> File3 datas_uploads_post(file=file)

Dépôt de fichier.

Permet de déposer un fichier dans un espace temporaire de NAKALA pour être ensuite associé à une donnée (requête POST /datas)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.file3 import File3
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    file = None # bytearray | Fichier à déposer (optional)

    try:
        # Dépôt de fichier.
        api_response = api_instance.datas_uploads_post(file=file)
        print("The response of DatasApi->datas_uploads_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DatasApi->datas_uploads_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file** | **bytearray**| Fichier à déposer | [optional] 

### Return type

[**File3**](File3.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Retourne l&#39;empreinte SHA1 du fichier déposé sur le serveur |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Clé d&#39;API non valide ou utilisateur inconnu |  -  |
**500** | Erreur lors de l&#39;enregistrement du fichier |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **embed_identifier_file_identifier_get**
> embed_identifier_file_identifier_get(identifier, file_identifier, buttons=buttons)

Visionneuse NAKALA du fichier \"fileIdentifier\" de la donnée \"identifier\".

Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    file_identifier = 'file_identifier_example' # str | Identifiant du fichier
    buttons = True # bool | Affichage dans la visionneuse des boutons de téléchargement et d'accès au fichier brut (optional)

    try:
        # Visionneuse NAKALA du fichier \"fileIdentifier\" de la donnée \"identifier\".
        api_instance.embed_identifier_file_identifier_get(identifier, file_identifier, buttons=buttons)
    except Exception as e:
        print("Exception when calling DatasApi->embed_identifier_file_identifier_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **file_identifier** | **str**| Identifiant du fichier | 
 **buttons** | **bool**| Affichage dans la visionneuse des boutons de téléchargement et d&#39;accès au fichier brut | [optional] 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Le contenu html de la visionneuse du fichier |  -  |
**500** | Erreur interne |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **iiif_identifier_file_identifier_info_json_get**
> iiif_identifier_file_identifier_info_json_get(identifier, file_identifier)

IIIF Image API - Information sur l'image \"fileIdentifier\" de la donnée \"identifier\".

Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    file_identifier = 'file_identifier_example' # str | Identifiant de l'image

    try:
        # IIIF Image API - Information sur l'image \"fileIdentifier\" de la donnée \"identifier\".
        api_instance.iiif_identifier_file_identifier_info_json_get(identifier, file_identifier)
    except Exception as e:
        print("Exception when calling DatasApi->iiif_identifier_file_identifier_info_json_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **file_identifier** | **str**| Identifiant de l&#39;image | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Les informations iiif de l&#39;image |  -  |
**401** | Donnée non publiée, clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas ou n&#39;est pas accessible |  -  |
**500** | Erreur interne |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **iiif_identifier_file_identifier_region_size_rotation_quality_format_get**
> iiif_identifier_file_identifier_region_size_rotation_quality_format_get(identifier, file_identifier, region, size, rotation, quality, format)

IIIF Image API - Transformation de l'image \"fileIdentifier\" de la donnée \"identifier\".

Pour accéder à la version spécifique d'une donnée, vous pouvez ajouter un numéro de version après l'identifiant de la donnée (ex: **10.34847/nkl.eabbbf68.v2** donne accès à la version 2 de la donnée **10.34847/nkl.eabbbf68**)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://apitest.nakala.fr
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://apitest.nakala.fr"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: apiKey
configuration.api_key['apiKey'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['apiKey'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DatasApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la donnée
    file_identifier = 'file_identifier_example' # str | Identifiant de l'image
    region = 'region_example' # str | Le paramètre région définit la partie rectangulaire du contenu de l'image sous-jacente à renvoyer.
    size = 'size_example' # str | Le paramètre size spécifie les dimensions auxquelles la région extraite, qui peut être l'image complète, doit être mise à l'échelle.
    rotation = 'rotation_example' # str | Le paramètre de rotation spécifie la mise en miroir et la rotation.
    quality = 'quality_example' # str | Le paramètre de qualité détermine si l'image est générée en couleur, en niveaux de gris ou en noir et blanc.
    format = 'format_example' # str | Le format de l'image renvoyée

    try:
        # IIIF Image API - Transformation de l'image \"fileIdentifier\" de la donnée \"identifier\".
        api_instance.iiif_identifier_file_identifier_region_size_rotation_quality_format_get(identifier, file_identifier, region, size, rotation, quality, format)
    except Exception as e:
        print("Exception when calling DatasApi->iiif_identifier_file_identifier_region_size_rotation_quality_format_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la donnée | 
 **file_identifier** | **str**| Identifiant de l&#39;image | 
 **region** | **str**| Le paramètre région définit la partie rectangulaire du contenu de l&#39;image sous-jacente à renvoyer. | 
 **size** | **str**| Le paramètre size spécifie les dimensions auxquelles la région extraite, qui peut être l&#39;image complète, doit être mise à l&#39;échelle. | 
 **rotation** | **str**| Le paramètre de rotation spécifie la mise en miroir et la rotation. | 
 **quality** | **str**| Le paramètre de qualité détermine si l&#39;image est générée en couleur, en niveaux de gris ou en noir et blanc. | 
 **format** | **str**| Le format de l&#39;image renvoyée | 

### Return type

void (empty response body)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | L&#39;image transformée suivant la requête à l&#39;api IIIF |  -  |
**401** | Donnée non publiée, clé d&#39;API manquante ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La donnée n&#39;existe pas ou n&#39;est pas accessible |  -  |
**500** | Erreur interne |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

