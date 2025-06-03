# openapi_client.UsersApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**users_collections_createdyears_get**](UsersApi.md#users_collections_createdyears_get) | **GET** /users/collections/createdyears | Récupération des différentes années de création des collections accessibles par un utilisateur.
[**users_collections_scope_post**](UsersApi.md#users_collections_scope_post) | **POST** /users/collections/{scope} | Récupération des collections accessibles par un utilisateur.
[**users_collections_statuses_get**](UsersApi.md#users_collections_statuses_get) | **GET** /users/collections/statuses | Récupération des différents statuts des collections accessibles par un utilisateur.
[**users_datas_createdyears_get**](UsersApi.md#users_datas_createdyears_get) | **GET** /users/datas/createdyears | Récupération des différentes années de création des données accessibles par un utilisateur.
[**users_datas_datatypes_get**](UsersApi.md#users_datas_datatypes_get) | **GET** /users/datas/datatypes | Récupération des types des données accessibles par un utilisateur.
[**users_datas_scope_post**](UsersApi.md#users_datas_scope_post) | **POST** /users/datas/{scope} | Récupération des données accessibles par un utilisateur.
[**users_datas_statuses_get**](UsersApi.md#users_datas_statuses_get) | **GET** /users/datas/statuses | Récupération des différents statuts des données accessibles par un utilisateur.
[**users_groups_scope_get**](UsersApi.md#users_groups_scope_get) | **GET** /users/groups/{scope} | Récupération des groupes d&#39;un utilisateur.
[**users_me_apikey_put**](UsersApi.md#users_me_apikey_put) | **PUT** /users/me/apikey | Mise à jour de la clé d&#39;API de l&#39;utilisateur courant.
[**users_me_get**](UsersApi.md#users_me_get) | **GET** /users/me | Récupération des informations sur l&#39;utilisateur courant.
[**users_me_put**](UsersApi.md#users_me_put) | **PUT** /users/me | Mise à jour des informations sur l&#39;utilisateur courant.
[**users_resources_identifier_action_get**](UsersApi.md#users_resources_identifier_action_get) | **GET** /users/resources/{identifier}/action | Demande d&#39;action sur une ressource.


# **users_collections_createdyears_get**
> List[str] users_collections_createdyears_get(scope=scope)

Récupération des différentes années de création des collections accessibles par un utilisateur.

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
    api_instance = openapi_client.UsersApi(api_client)
    scope = all # str | Périmètre des collections (optional) (default to all)

    try:
        # Récupération des différentes années de création des collections accessibles par un utilisateur.
        api_response = api_instance.users_collections_createdyears_get(scope=scope)
        print("The response of UsersApi->users_collections_createdyears_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_collections_createdyears_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des collections | [optional] [default to all]

### Return type

**List[str]**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des années de création des collections accessibles par l&#39;utilisateur |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_collections_scope_post**
> UsersCollectionsScopePost200Response users_collections_scope_post(scope, body=body)

Récupération des collections accessibles par un utilisateur.

Retourne les collections d'un utilisateur en fonction du périmètre choisi :
- `deposited` : les collections déposées par l'utilisateur (ROLE_DEPOSITOR)
- `owned` : les collections dont l'utilisateur est propriétaire (ROLE_OWNER)
- `shared` : les collections partagées avec l'utilisateur (ROLE_ADMIN, ROLE_EDITOR ou ROLE_READER, mais pas ROLE_OWNER)
- `editable` : les collections modifiables par l'utilisateur (ROLE_OWNER, ROLE_ADMIN ou ROLE_EDITOR)
- `readable` : les collections lisibles par l'utilisateur (ROLE_OWNER, ROLE_ADMIN, ROLE_EDITOR ou ROLE_READER)
- `all` : toutes les collections auxquelles l'utilisateur à accès (ROLE_OWNER, ROLE_ADMIN, ROLE_EDITOR ou ROLE_READER) ainsi que toutes les collections publiques de NAKALA

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.user_collections_query import UserCollectionsQuery
from openapi_client.models.users_collections_scope_post200_response import UsersCollectionsScopePost200Response
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
    api_instance = openapi_client.UsersApi(api_client)
    scope = 'scope_example' # str | Périmètre des collections
    body = openapi_client.UserCollectionsQuery() # UserCollectionsQuery |  (optional)

    try:
        # Récupération des collections accessibles par un utilisateur.
        api_response = api_instance.users_collections_scope_post(scope, body=body)
        print("The response of UsersApi->users_collections_scope_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_collections_scope_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des collections | 
 **body** | [**UserCollectionsQuery**](UserCollectionsQuery.md)|  | [optional] 

### Return type

[**UsersCollectionsScopePost200Response**](UsersCollectionsScopePost200Response.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retourne la liste des collections de l&#39;utilisateur |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Utilisateur non autorisé |  -  |
**404** | L&#39;utilisateur demandé n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_collections_statuses_get**
> List[str] users_collections_statuses_get(scope=scope)

Récupération des différents statuts des collections accessibles par un utilisateur.

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
    api_instance = openapi_client.UsersApi(api_client)
    scope = all # str | Périmètre des collections (optional) (default to all)

    try:
        # Récupération des différents statuts des collections accessibles par un utilisateur.
        api_response = api_instance.users_collections_statuses_get(scope=scope)
        print("The response of UsersApi->users_collections_statuses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_collections_statuses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des collections | [optional] [default to all]

### Return type

**List[str]**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des statuts des collections accessibles par l&#39;utilisateur |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_datas_createdyears_get**
> List[str] users_datas_createdyears_get(scope=scope, collections=collections)

Récupération des différentes années de création des données accessibles par un utilisateur.

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
    api_instance = openapi_client.UsersApi(api_client)
    scope = all # str | Périmètre des données (optional) (default to all)
    collections = ['collections_example'] # List[str] | Identifiants des collections auxquelles peuvent appartenir les données (optional)

    try:
        # Récupération des différentes années de création des données accessibles par un utilisateur.
        api_response = api_instance.users_datas_createdyears_get(scope=scope, collections=collections)
        print("The response of UsersApi->users_datas_createdyears_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_datas_createdyears_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des données | [optional] [default to all]
 **collections** | [**List[str]**](str.md)| Identifiants des collections auxquelles peuvent appartenir les données | [optional] 

### Return type

**List[str]**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des années de création des données utilisateur concernées par le périmètre |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_datas_datatypes_get**
> List[str] users_datas_datatypes_get(scope=scope, collections=collections)

Récupération des types des données accessibles par un utilisateur.

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
    api_instance = openapi_client.UsersApi(api_client)
    scope = all # str | Périmètre des données (optional) (default to all)
    collections = ['collections_example'] # List[str] | Identifiants des collections auxquelles peuvent appartenir les données (optional)

    try:
        # Récupération des types des données accessibles par un utilisateur.
        api_response = api_instance.users_datas_datatypes_get(scope=scope, collections=collections)
        print("The response of UsersApi->users_datas_datatypes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_datas_datatypes_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des données | [optional] [default to all]
 **collections** | [**List[str]**](str.md)| Identifiants des collections auxquelles peuvent appartenir les données | [optional] 

### Return type

**List[str]**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des types des données possédées par l&#39;utilisateur |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_datas_scope_post**
> UsersDatasScopePost200Response users_datas_scope_post(scope, body=body)

Récupération des données accessibles par un utilisateur.

Retourne les données d'un utilisateur en fonction du périmètre choisi :
- `deposited` : les données déposées par l'utilisateur (ROLE_DEPOSITOR)
- `owned` : les données dont l'utilisateur est propriétaire (ROLE_OWNER)
- `shared` : les données partagées avec l'utilisateur (ROLE_ADMIN, ROLE_EDITOR ou ROLE_READER, mais pas ROLE_OWNER)
- `editable` : les données modifiables par l'utilisateur (ROLE_OWNER, ROLE_ADMIN ou ROLE_EDITOR)
- `readable` : les données lisibles par l'utilisateur (ROLE_OWNER, ROLE_ADMIN, ROLE_EDITOR ou ROLE_READER)
- `moderable` : les données modérables par l'utilisateur (ROLE_MODERATOR)
- `all` : toutes les données auxquelles l'utilisateur à accès (ROLE_OWNER, ROLE_ADMIN, ROLE_EDITOR, ROLE_READER ou ROLE_MODERATOR) ainsi que toutes les données publiées de NAKALA

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.user_datas_query import UserDatasQuery
from openapi_client.models.users_datas_scope_post200_response import UsersDatasScopePost200Response
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
    api_instance = openapi_client.UsersApi(api_client)
    scope = 'scope_example' # str | Périmètre des données
    body = openapi_client.UserDatasQuery() # UserDatasQuery |  (optional)

    try:
        # Récupération des données accessibles par un utilisateur.
        api_response = api_instance.users_datas_scope_post(scope, body=body)
        print("The response of UsersApi->users_datas_scope_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_datas_scope_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des données | 
 **body** | [**UserDatasQuery**](UserDatasQuery.md)|  | [optional] 

### Return type

[**UsersDatasScopePost200Response**](UsersDatasScopePost200Response.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retourne la liste des données de l&#39;utilisateur |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Utilisateur non autorisé |  -  |
**404** | L&#39;utilisateur demandé n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_datas_statuses_get**
> List[str] users_datas_statuses_get(scope=scope, collections=collections)

Récupération des différents statuts des données accessibles par un utilisateur.

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
    api_instance = openapi_client.UsersApi(api_client)
    scope = all # str | Périmètre des données (optional) (default to all)
    collections = ['collections_example'] # List[str] | Identifiants des collections auxquelles peuvent appartenir les données (optional)

    try:
        # Récupération des différents statuts des données accessibles par un utilisateur.
        api_response = api_instance.users_datas_statuses_get(scope=scope, collections=collections)
        print("The response of UsersApi->users_datas_statuses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_datas_statuses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des données | [optional] [default to all]
 **collections** | [**List[str]**](str.md)| Identifiants des collections auxquelles peuvent appartenir les données | [optional] 

### Return type

**List[str]**

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des statuts des données utilisateur concernées par le périmètre |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_groups_scope_get**
> List[DetailedMultiUserGroup] users_groups_scope_get(scope, q=q, page=page, limit=limit, order=order)

Récupération des groupes d'un utilisateur.

Retourne les groupes d'un utilisateur en fonction des ensembles suivants :
- `owned` : les groupes créés par l'utilisateur
- `shared` : les groupes créés par d'autres utilisateurs et incluant l'utilisateur
- `all` : tous les groupes créer par l'utilisateur ou incluant l'utilisateur

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.detailed_multi_user_group import DetailedMultiUserGroup
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
    api_instance = openapi_client.UsersApi(api_client)
    scope = 'scope_example' # str | Périmètre des groupes
    q = 'q_example' # str | Mot clé pour la recherche (optional)
    page = '1' # str | Page courante (optional) (default to '1')
    limit = '10' # str | Nombre de résultats par page (optional) (default to '10')
    order = 'datemodify,desc' # str | Tri des résultats (optional) (default to 'datemodify,desc')

    try:
        # Récupération des groupes d'un utilisateur.
        api_response = api_instance.users_groups_scope_get(scope, q=q, page=page, limit=limit, order=order)
        print("The response of UsersApi->users_groups_scope_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_groups_scope_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **scope** | **str**| Périmètre des groupes | 
 **q** | **str**| Mot clé pour la recherche | [optional] 
 **page** | **str**| Page courante | [optional] [default to &#39;1&#39;]
 **limit** | **str**| Nombre de résultats par page | [optional] [default to &#39;10&#39;]
 **order** | **str**| Tri des résultats | [optional] [default to &#39;datemodify,desc&#39;]

### Return type

[**List[DetailedMultiUserGroup]**](DetailedMultiUserGroup.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Une liste de groupes d&#39;utilisateurs |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | Utilisateur non autorisé |  -  |
**404** | L&#39;utilisateur demandé n&#39;existe pas |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_me_apikey_put**
> UsersMeApikeyPut200Response users_me_apikey_put()

Mise à jour de la clé d'API de l'utilisateur courant.

Permet de mettre à jour la clé d'API de l'utilisateur courant

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.users_me_apikey_put200_response import UsersMeApikeyPut200Response
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
    api_instance = openapi_client.UsersApi(api_client)

    try:
        # Mise à jour de la clé d'API de l'utilisateur courant.
        api_response = api_instance.users_me_apikey_put()
        print("The response of UsersApi->users_me_apikey_put:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_me_apikey_put: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UsersMeApikeyPut200Response**](UsersMeApikeyPut200Response.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | La clé d&#39;API de l&#39;utilisateur a bien été mise à jour |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | La clé d&#39;API ne correspond à aucun utilisateur connu |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_me_get**
> User users_me_get()

Récupération des informations sur l'utilisateur courant.

Retourne l'ensemble des informations disponibles sur l'utilisateur courant

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.user import User
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
    api_instance = openapi_client.UsersApi(api_client)

    try:
        # Récupération des informations sur l'utilisateur courant.
        api_response = api_instance.users_me_get()
        print("The response of UsersApi->users_me_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_me_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Informations sur l&#39;utilisateur courant |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | La clé d&#39;API ne correspond à aucun utilisateur connu |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_me_put**
> users_me_put(user=user)

Mise à jour des informations sur l'utilisateur courant.

Permet de mettre à jour les informations sur l'utilisateur courant

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.user2 import User2
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
    api_instance = openapi_client.UsersApi(api_client)
    user = openapi_client.User2() # User2 | Nouvelles données sur l'utilisateur (optional)

    try:
        # Mise à jour des informations sur l'utilisateur courant.
        api_instance.users_me_put(user=user)
    except Exception as e:
        print("Exception when calling UsersApi->users_me_put: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user** | [**User2**](User2.md)| Nouvelles données sur l&#39;utilisateur | [optional] 

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
**200** | Les données de l&#39;utilisateur courant ont bien été mises à jour |  -  |
**401** | Clé d&#39;API manquante ou invalide, compte utilisateur inexistant |  -  |
**403** | La clé d&#39;API ne correspond à aucun utilisateur connu |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **users_resources_identifier_action_get**
> List[Task] users_resources_identifier_action_get(identifier)

Demande d'action sur une ressource.

### Example

* Api Key Authentication (apiKey):

```python
import openapi_client
from openapi_client.models.task import Task
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
    api_instance = openapi_client.UsersApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la ressource

    try:
        # Demande d'action sur une ressource.
        api_response = api_instance.users_resources_identifier_action_get(identifier)
        print("The response of UsersApi->users_resources_identifier_action_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UsersApi->users_resources_identifier_action_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la ressource | 

### Return type

[**List[Task]**](Task.md)

### Authorization

[apiKey](../README.md#apiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Les actions attribuées sur cette ressource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

