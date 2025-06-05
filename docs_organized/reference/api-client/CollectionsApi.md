# openapi_client.CollectionsApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**collections_identifier_datas_delete**](CollectionsApi.md#collections_identifier_datas_delete) | **DELETE** /collections/{identifier}/datas | Suppression d&#39;une liste de données d&#39;une collection.
[**collections_identifier_datas_get**](CollectionsApi.md#collections_identifier_datas_get) | **GET** /collections/{identifier}/datas | Récupération de la liste paginée des données contenues dans la collection.
[**collections_identifier_datas_post**](CollectionsApi.md#collections_identifier_datas_post) | **POST** /collections/{identifier}/datas | Ajout d&#39;une liste de données dans une collection.
[**collections_identifier_delete**](CollectionsApi.md#collections_identifier_delete) | **DELETE** /collections/{identifier} | Suppression d&#39;une collection.
[**collections_identifier_get**](CollectionsApi.md#collections_identifier_get) | **GET** /collections/{identifier} | Récupération des informations sur une collection.
[**collections_identifier_metadatas_delete**](CollectionsApi.md#collections_identifier_metadatas_delete) | **DELETE** /collections/{identifier}/metadatas | Suppression de métadonnées pour une collection.
[**collections_identifier_metadatas_get**](CollectionsApi.md#collections_identifier_metadatas_get) | **GET** /collections/{identifier}/metadatas | Récupération des métadonnées d&#39;une collection.
[**collections_identifier_metadatas_post**](CollectionsApi.md#collections_identifier_metadatas_post) | **POST** /collections/{identifier}/metadatas | Ajout d&#39;une nouvelle métadonnée à une collection.
[**collections_identifier_put**](CollectionsApi.md#collections_identifier_put) | **PUT** /collections/{identifier} | Modification des informations d&#39;une collection.
[**collections_identifier_rights_delete**](CollectionsApi.md#collections_identifier_rights_delete) | **DELETE** /collections/{identifier}/rights | Suppression des droits pour utilisateur ou un groupe d&#39;utilisateurs sur une collection.
[**collections_identifier_rights_get**](CollectionsApi.md#collections_identifier_rights_get) | **GET** /collections/{identifier}/rights | Récupération des utilisateurs et des groupes ayant des droits sur la collection.
[**collections_identifier_rights_post**](CollectionsApi.md#collections_identifier_rights_post) | **POST** /collections/{identifier}/rights | Ajout de droits sur une collection.
[**collections_identifier_status_get**](CollectionsApi.md#collections_identifier_status_get) | **GET** /collections/{identifier}/status | Récupération du statut d&#39;une collection.
[**collections_identifier_status_status_put**](CollectionsApi.md#collections_identifier_status_status_put) | **PUT** /collections/{identifier}/status/{status} | Changement du statut d&#39;une collection.
[**collections_post**](CollectionsApi.md#collections_post) | **POST** /collections | Création d&#39;une nouvelle collection.


# **collections_identifier_datas_delete**
> collections_identifier_datas_delete(identifier, datas)

Suppression d'une liste de données d'une collection.

L'utilisateur doit être au minimum éditeur de la collection et avoir les droits de lecture sur les données.
Ni la collection, ni les données ne sont supprimées de NAKALA.

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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    datas = ['datas_example'] # List[str] | Liste des identifiants des données à supprimer de la collection

    try:
        # Suppression d'une liste de données d'une collection.
        api_instance.collections_identifier_datas_delete(identifier, datas)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_datas_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **datas** | [**List[str]**](str.md)| Liste des identifiants des données à supprimer de la collection | 

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
**200** | Les données ont été supprimées de la collection |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Droits insuffisants pour supprimer les données de la collection |  -  |
**404** | Collection ou donnée non trouvée |  -  |
**500** | Erreur lors de la suppression des données de la collection |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_datas_get**
> CollectionsIdentifierDatasGet200Response collections_identifier_datas_get(identifier, page=page, limit=limit)

Récupération de la liste paginée des données contenues dans la collection.

Une clé d'API et les droits sur la collection sont nécessaires pour les collections privées

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.collections_identifier_datas_get200_response import CollectionsIdentifierDatasGet200Response
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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    page = 1 # int | La page souhaitée (optional) (default to 1)
    limit = 10 # int | Le nombre de résultat par page (optional) (default to 10)

    try:
        # Récupération de la liste paginée des données contenues dans la collection.
        api_response = api_instance.collections_identifier_datas_get(identifier, page=page, limit=limit)
        print("The response of CollectionsApi->collections_identifier_datas_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_datas_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **page** | **int**| La page souhaitée | [optional] [default to 1]
 **limit** | **int**| Le nombre de résultat par page | [optional] [default to 10]

### Return type

[**CollectionsIdentifierDatasGet200Response**](CollectionsIdentifierDatasGet200Response.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | La liste paginée des données |  -  |
**401** | Collection privée, nécessite une clé d&#39;API et les droits sur la collection |  -  |
**403** | Collection privée, nécessite les droits dessus |  -  |
**404** | Aucune collection n&#39;existe pour cet identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_datas_post**
> collections_identifier_datas_post(identifier, datas)

Ajout d'une liste de données dans une collection.

L'utilisateur doit être au minimum éditeur de la collection et avoir les droits de lecture sur les données
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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    datas = ['datas_example'] # List[str] | Liste des identifiants des données à ajouter à la collection

    try:
        # Ajout d'une liste de données dans une collection.
        api_instance.collections_identifier_datas_post(identifier, datas)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_datas_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **datas** | [**List[str]**](str.md)| Liste des identifiants des données à ajouter à la collection | 

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
**201** | Les données ont été ajoutées à la collection |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Droits insuffisants pour ajouter les données dans la collection |  -  |
**404** | Collection ou donnée non trouvée |  -  |
**500** | Erreur lors de l&#39;ajout des données dans la collection |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_delete**
> collections_identifier_delete(identifier)

Suppression d'une collection.

Supprime définitivement la collection.
Les données contenues dans la collection ne seront pas supprimées

Attention : Il est possible de ne supprimer que certaines informations de la collection
Pour cela, vous pouvez utiliser les routes spécifiques (ex: /collections/{identifier}/rights)
Vous pouvez aussi effectuer une modification partielle d'une collection (ex: cf. PUT /collections/{identifier})

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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection

    try:
        # Suppression d'une collection.
        api_instance.collections_identifier_delete(identifier)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 

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
**204** | La collection a été supprimée |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Compte utilisateur non trouvé |  -  |
**404** | Aucune collection n&#39;existe avec cet identifiant |  -  |
**500** | Erreur lors de la suppression de la collection |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_get**
> Collection3 collections_identifier_get(identifier, metadata_format=metadata_format)

Récupération des informations sur une collection.

Retourne l'ensemble des informations d'une collection
- Métadonnées techniques de la collection (statut, propriétaire, etc.)
- Métadonnées descriptives de la collection

Si la clé d'API est transmise, et que vous avez les droits sur la
collection, les informations privées seront également retournées

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.collection3 import Collection3
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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    metadata_format = 'metadata_format_example' # str | format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) (optional)

    try:
        # Récupération des informations sur une collection.
        api_response = api_instance.collections_identifier_get(identifier, metadata_format=metadata_format)
        print("The response of CollectionsApi->collections_identifier_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **metadata_format** | **str**| format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) | [optional] 

### Return type

[**Collection3**](Collection3.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Informations sur la collection |  -  |
**401** | La collection est privée et nécessite une authentification |  -  |
**403** | Accès interdit (mauvaise clé d&#39;API ou droits insuffisants) |  -  |
**404** | Aucune collection n&#39;existe avec cet identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_metadatas_delete**
> collections_identifier_metadatas_delete(identifier, meta=meta)

Suppression de métadonnées pour une collection.

Toutes les métadonnées correspondant au modèle transmis seront supprimées. Par exemple
- Pour supprimer tous les <dcterms:subject>
```
{"propertyUri": "http://purl.org/dc/terms/subject"}
```
- Pour supprimer les métadonnées en anglais
```
{"lang": "en"}
```
- Pour supprimer les <dcterms:subject> en anglais :
```
{"lang": "en", "propertyUri": "http://purl.org/dc/terms/subject"}
```

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.meta3 import Meta3
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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    meta = openapi_client.Meta3() # Meta3 | Modèle de métadonnées à supprimer (optional)

    try:
        # Suppression de métadonnées pour une collection.
        api_instance.collections_identifier_metadatas_delete(identifier, meta=meta)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_metadatas_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **meta** | [**Meta3**](Meta3.md)| Modèle de métadonnées à supprimer | [optional] 

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
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Utilisateur non trouvé ou droits insuffisants |  -  |
**404** | Aucune collection trouvée à partir de l&#39;identifiant |  -  |
**500** | Erreur lors de la suppression de métadonnées |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_metadatas_get**
> List[Meta3] collections_identifier_metadatas_get(identifier, metadata_format=metadata_format)

Récupération des métadonnées d'une collection.

Retourne les métadonnées descriptives de la collection

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.meta3 import Meta3
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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    metadata_format = 'metadata_format_example' # str | format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) (optional)

    try:
        # Récupération des métadonnées d'une collection.
        api_response = api_instance.collections_identifier_metadatas_get(identifier, metadata_format=metadata_format)
        print("The response of CollectionsApi->collections_identifier_metadatas_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_metadatas_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **metadata_format** | **str**| format des métadonnées (Attention ! Le format dc est déprécié et sera retiré prochainement) | [optional] 

### Return type

[**List[Meta3]**](Meta3.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste de métadonnées |  -  |
**401** | Collection privée, nécessite que l&#39;utilisateur dispose de droits sur la collection |  -  |
**403** | Collection privée, droits manquants sur la collection |  -  |
**404** | Aucune collection trouvée à partir de l&#39;identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_metadatas_post**
> collections_identifier_metadatas_post(identifier, meta=meta)

Ajout d'une nouvelle métadonnée à une collection.

Permet d'ajouter une métadonnée descriptive de la collection
La métadonnée contient
- une propriété
- une valeur (string ou objet auteur)
- un type (optionnel)
- un format (optionnel)

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.meta3 import Meta3
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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    meta = openapi_client.Meta3() # Meta3 | Métadonnée à ajouter (optional)

    try:
        # Ajout d'une nouvelle métadonnée à une collection.
        api_instance.collections_identifier_metadatas_post(identifier, meta=meta)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_metadatas_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **meta** | [**Meta3**](Meta3.md)| Métadonnée à ajouter | [optional] 

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
**201** | La métadonnée a été ajoutée à la collection |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Utilisateur non trouvé ou droits insuffisants pour modifier la collection |  -  |
**404** | Aucune collection trouvée à partir de l&#39;identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_put**
> collections_identifier_put(identifier, collection=collection)

Modification des informations d'une collection.

La collection transmise remplacera celle déja existante.
Chaque entrée (rights, metas, status, datas) est facultative, mais doit contenir une liste exhaustive.
Si vous souhaitez par exemple modifier une seule métadonnée, vous devrez renseigner l'ensemble des métadonnées précédentes en plus de celle portant la modification.
Vous pouvez vider l'ensemble des données pour "rights" et "datas" en soumettant un tableau vide.

L'édition des champs "metas" et "datas" requière le ROLE_EDITOR et l'édition des champs "status" et "rights" requière le ROLE_ADMIN.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.collection4 import Collection4
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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    collection = openapi_client.Collection4() # Collection4 | Collection à modifier (optional)

    try:
        # Modification des informations d'une collection.
        api_instance.collections_identifier_put(identifier, collection=collection)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **collection** | [**Collection4**](Collection4.md)| Collection à modifier | [optional] 

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
**204** | La collection a été modifiée |  -  |
**401** | Clé d&#39;API manquante ou invalide |  -  |
**403** | Compte utilisateur inexistant ou droits sur la collection insuffisants |  -  |
**404** | Aucune collection n&#39;existe avec cet identifiant |  -  |
**500** | Erreur lors de l&#39;enregistrement de la collection |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_rights_delete**
> collections_identifier_rights_delete(identifier, right=right)

Suppression des droits pour utilisateur ou un groupe d'utilisateurs sur une collection.

La suppression des droits d'une collection est autorisée aux utilisateurs ayant les droits propriétaire ou administrateur.
Il est possible de passer un filtre dans le corps de la requête qui permettra de ne supprimer que certains droits.
Par exemple pour supprimer tous les éditeurs d'une collection :
```
{"role": "ROLE_EDITOR"}
```
Note: le droit **propriétaire** (ROLE_OWNER) d'une collection ne peut pas être supprimé.

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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    right = openapi_client.DeleteRight() # DeleteRight | Droit à supprimer (optional)

    try:
        # Suppression des droits pour utilisateur ou un groupe d'utilisateurs sur une collection.
        api_instance.collections_identifier_rights_delete(identifier, right=right)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_rights_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
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
**404** | La collection n&#39;existe pas |  -  |
**500** | Erreur lors de la suppression du droit |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_rights_get**
> List[DetailedRight] collections_identifier_rights_get(identifier)

Récupération des utilisateurs et des groupes ayant des droits sur la collection.

Permet de retourner une liste contenant
- l'utilisateur ou le groupe d'utilisateurs
- le droit sur la collection
  - **propriétaire** (ROLE_OWNER) : consultation, modification, suppression, partage des droits de la donnée
  - **administrateur** (ROLE_ADMIN) : consultation, modification, suppression, partage des droits de la donnée
  - **editeur** (ROLE_EDITOR) :  consultation, modification, suppression de la donnée
  - **lecteur** (ROLE_READER) :  consultation de la donnée
Note: Seule la personne ayant déposé la collection peut avoir les droits propriétaires.

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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection

    try:
        # Récupération des utilisateurs et des groupes ayant des droits sur la collection.
        api_response = api_instance.collections_identifier_rights_get(identifier)
        print("The response of CollectionsApi->collections_identifier_rights_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_rights_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 

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
**200** | Liste des utilisateurs et des groupes ayant des droits sur la collection |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**404** | La collection n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_rights_post**
> collections_identifier_rights_post(identifier, rights=rights)

Ajout de droits sur une collection.

Permet de rajouter des droits à un utilisateur ou un group d'utilisateurs sur une collection.
Les droits possibles sont :
- **administrateur** (ROLE_ADMIN) : consultation, modification, suppression, partage des droits de la collection
- **éditeur** (ROLE_EDITOR) : consultation, modification de la collection
- **lecteur** (ROLE_READER) : consultation de la collection même si elle est privée
Note: Le droit **propriétaire** (ROLE_OWNER) est attribué automatiquement au déposant de la collection et ne peut pas être attribué à une autre utilisateur

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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    rights = [openapi_client.PostRight()] # List[PostRight] | tableau des nouveaux droits à ajouter à la collection (optional)

    try:
        # Ajout de droits sur une collection.
        api_instance.collections_identifier_rights_post(identifier, rights=rights)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_rights_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **rights** | [**List[PostRight]**](PostRight.md)| tableau des nouveaux droits à ajouter à la collection | [optional] 

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
**200** | Droits ajoutés sur la collection |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Droit sur la donnée insuffisant |  -  |
**404** | La collection n&#39;existe pas |  -  |
**500** | Erreur lors de l&#39;ajout du droit sur la collection |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_status_get**
> collections_identifier_status_get(identifier)

Récupération du statut d'une collection.

Permet de savoir si une collection est privée ou publique

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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection

    try:
        # Récupération du statut d'une collection.
        api_instance.collections_identifier_status_get(identifier)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_status_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 

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
**200** | Statut de la collection |  -  |
**404** | La collection n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_identifier_status_status_put**
> collections_identifier_status_status_put(identifier, status)

Changement du statut d'une collection.

Permet de gérer le statut de la collection (private ou public)
Une collection publique ne peut avoir que des données publiées

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
    api_instance = openapi_client.CollectionsApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la collection
    status = 'status_example' # str | Nouveau statut de la collection

    try:
        # Changement du statut d'une collection.
        api_instance.collections_identifier_status_status_put(identifier, status)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_identifier_status_status_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la collection | 
 **status** | **str**| Nouveau statut de la collection | 

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
**204** | Le nouveau statut a été enregistré |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Compte utilisateur non trouvé ou droits sur la collection insuffisants |  -  |
**404** | Aucune collection n&#39;existe avec cet identifiant |  -  |
**500** | Erreur lors de l&#39;enregistrement de la donnée |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **collections_post**
> collections_post(collection=collection)

Création d'une nouvelle collection.

Les informations suivantes sont à transmettre

- Statut de la collection (private ou public)
- Liste des identifiants des données à ajouter à la collection. Une
collection publique ne peut contenir que des données publiées.
- Métadonnées descriptives de la collection :
lang : la liste des valeurs acceptées est disponible via GET
/vocabularies/languages typeUri : la liste des valeurs acceptées est
disponible via GET /vocabularies/metadatatypes propertyUri : la liste
des valeurs acceptées est disponible via GET /vocabularies/properties La
métadonnée http://nakala.fr/terms#title est obligatoire.
- Partage de droits sur cette collection

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.collection import Collection
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
    api_instance = openapi_client.CollectionsApi(api_client)
    collection = openapi_client.Collection() # Collection | Informations sur la collection à créer (optional)

    try:
        # Création d'une nouvelle collection.
        api_instance.collections_post(collection=collection)
    except Exception as e:
        print("Exception when calling CollectionsApi->collections_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection** | [**Collection**](Collection.md)| Informations sur la collection à créer | [optional] 

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
**201** | La collection a été correctement créée |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Utilisateur non autorisé |  -  |
**500** | Erreur lors de l&#39;enregistrement de la collection |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

