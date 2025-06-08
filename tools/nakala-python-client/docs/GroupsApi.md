# openapi_client.GroupsApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**groups_id_delete**](GroupsApi.md#groups_id_delete) | **DELETE** /groups/{id} | Suppression d&#39;un groupe d&#39;utilisateurs.
[**groups_id_get**](GroupsApi.md#groups_id_get) | **GET** /groups/{id} | Récupération des informations sur un groupe d&#39;utilisateurs.
[**groups_id_put**](GroupsApi.md#groups_id_put) | **PUT** /groups/{id} | Modification d&#39;un groupe d&#39;utilisateurs.
[**groups_post**](GroupsApi.md#groups_post) | **POST** /groups | Création d&#39;un nouveau groupe d&#39;utilisateurs.
[**groups_search_get**](GroupsApi.md#groups_search_get) | **GET** /groups/search | Récupération des utilisateurs et groupes d&#39;utilisateurs.


# **groups_id_delete**
> groups_id_delete(id)

Suppression d'un groupe d'utilisateurs.

La suppression d'un groupe entraine la suppression de tous les droits liés à ce groupe.
Note: Il n'est pas possible de supprimer un groupe de type "user" ou un groupe propriétaire d'une donnée ou d'une collection

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
    api_instance = openapi_client.GroupsApi(api_client)
    id = 'id_example' # str | Identifiant du groupe

    try:
        # Suppression d'un groupe d'utilisateurs.
        api_instance.groups_id_delete(id)
    except Exception as e:
        print("Exception when calling GroupsApi->groups_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identifiant du groupe | 

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
**200** | Groupe supprimé |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**403** | Groupe inaccessible |  -  |
**404** | Aucun groupe n&#39;existe avec cet identifiant |  -  |
**500** | Erreur lors de la suppression du groupe |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_id_get**
> DetailedAbstractGroup groups_id_get(id)

Récupération des informations sur un groupe d'utilisateurs.

Retourne l'ensemble des informations relatives à un groupe d'utilisateurs

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.detailed_abstract_group import DetailedAbstractGroup
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
    api_instance = openapi_client.GroupsApi(api_client)
    id = 'id_example' # str | Identifiant du groupe

    try:
        # Récupération des informations sur un groupe d'utilisateurs.
        api_response = api_instance.groups_id_get(id)
        print("The response of GroupsApi->groups_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->groups_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identifiant du groupe | 

### Return type

[**DetailedAbstractGroup**](DetailedAbstractGroup.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Un groupe d&#39;utilisateurs |  -  |
**403** | Groupe inaccessible |  -  |
**404** | Aucun groupe n&#39;existe avec cet identifiant |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_id_put**
> groups_id_put(id, group=group)

Modification d'un groupe d'utilisateurs.

Le groupe transmis remplacera celui déjà existant.
Note: Il n'est pas possible de modifier des groupes de type "user".

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.post_and_put_group import PostAndPutGroup
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
    api_instance = openapi_client.GroupsApi(api_client)
    id = 'id_example' # str | Identifiant du groupe
    group = openapi_client.PostAndPutGroup() # PostAndPutGroup | Groupe d'utilisateurs à modifier (optional)

    try:
        # Modification d'un groupe d'utilisateurs.
        api_instance.groups_id_put(id, group=group)
    except Exception as e:
        print("Exception when calling GroupsApi->groups_id_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Identifiant du groupe | 
 **group** | [**PostAndPutGroup**](PostAndPutGroup.md)| Groupe d&#39;utilisateurs à modifier | [optional] 

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
**200** | Le groupe a été modifiée |  -  |
**401** | Clé d&#39;API manquante ou invalide |  -  |
**403** | Compte utilisateur inexistant |  -  |
**404** | Aucun groupe n&#39;existe avec cet identifiant |  -  |
**500** | Erreur lors de l&#39;enregistrement du groupe |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_post**
> groups_post(group=group)

Création d'un nouveau groupe d'utilisateurs.

Permet de créer un groupe d'utilisateurs.
Note: L'utilisateur créant le groupe est ajouté automatiquement parmi les membres avec le ROLE_OWNER.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.post_and_put_group import PostAndPutGroup
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
    api_instance = openapi_client.GroupsApi(api_client)
    group = openapi_client.PostAndPutGroup() # PostAndPutGroup | Nouveau groupe d'utilisateurs (optional)

    try:
        # Création d'un nouveau groupe d'utilisateurs.
        api_instance.groups_post(group=group)
    except Exception as e:
        print("Exception when calling GroupsApi->groups_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group** | [**PostAndPutGroup**](PostAndPutGroup.md)| Nouveau groupe d&#39;utilisateurs | [optional] 

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
**201** | Enregistrement du groupe |  -  |
**401** | Erreur d&#39;authentification (mauvaise clé d&#39;API) ou compte utilisateur inexistant |  -  |
**404** | Compte utilisateur inexistant |  -  |
**500** | Erreur lors de l&#39;enregistrement du groupe |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **groups_search_get**
> List[DetailedAbstractGroup] groups_search_get(q=q, order=order, page=page, limit=limit)

Récupération des utilisateurs et groupes d'utilisateurs.

Retourne des utilisateurs et groupes d'utilisateurs en fonction de critères de recherche

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.detailed_abstract_group import DetailedAbstractGroup
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
    api_instance = openapi_client.GroupsApi(api_client)
    q = 'q_example' # str | Mot clé pour la recherche (optional)
    order = 'asc' # str | Sens du tri (basé le prénom puis le nom de famille) (optional) (default to 'asc')
    page = '1' # str | Page courante (optional) (default to '1')
    limit = '10' # str | Nombre de résultats par page (optional) (default to '10')

    try:
        # Récupération des utilisateurs et groupes d'utilisateurs.
        api_response = api_instance.groups_search_get(q=q, order=order, page=page, limit=limit)
        print("The response of GroupsApi->groups_search_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GroupsApi->groups_search_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Mot clé pour la recherche | [optional] 
 **order** | **str**| Sens du tri (basé le prénom puis le nom de famille) | [optional] [default to &#39;asc&#39;]
 **page** | **str**| Page courante | [optional] [default to &#39;1&#39;]
 **limit** | **str**| Nombre de résultats par page | [optional] [default to &#39;10&#39;]

### Return type

[**List[DetailedAbstractGroup]**](DetailedAbstractGroup.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Une liste d&#39;utilisateurs et groupes d&#39;utilisateurs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

