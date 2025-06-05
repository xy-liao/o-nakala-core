# openapi_client.VocabulariesApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**vocabularies_collection_statuses_get**](VocabulariesApi.md#vocabularies_collection_statuses_get) | **GET** /vocabularies/collectionStatuses | Récupération des statuts des collections de Nakala.
[**vocabularies_country_codes_get**](VocabulariesApi.md#vocabularies_country_codes_get) | **GET** /vocabularies/countryCodes | Récupération des codes pays ISO 3166 (alpha-2).
[**vocabularies_data_statuses_get**](VocabulariesApi.md#vocabularies_data_statuses_get) | **GET** /vocabularies/dataStatuses | Récupération des statuts des données de Nakala.
[**vocabularies_datatypes_get**](VocabulariesApi.md#vocabularies_datatypes_get) | **GET** /vocabularies/datatypes | Récupération des types des données de Nakala.
[**vocabularies_dcmitypes_get**](VocabulariesApi.md#vocabularies_dcmitypes_get) | **GET** /vocabularies/dcmitypes | Récupération des types DCMI.
[**vocabularies_languages_get**](VocabulariesApi.md#vocabularies_languages_get) | **GET** /vocabularies/languages | Récupération des langues des métadonnées.
[**vocabularies_licenses_get**](VocabulariesApi.md#vocabularies_licenses_get) | **GET** /vocabularies/licenses | Récupération des licences des données de Nakala.
[**vocabularies_metadatatypes_get**](VocabulariesApi.md#vocabularies_metadatatypes_get) | **GET** /vocabularies/metadatatypes | Récupération des types des métadonnées.
[**vocabularies_properties_get**](VocabulariesApi.md#vocabularies_properties_get) | **GET** /vocabularies/properties | Récupération des propriétés des métadonnées.


# **vocabularies_collection_statuses_get**
> List[str] vocabularies_collection_statuses_get()

Récupération des statuts des collections de Nakala.

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
    api_instance = openapi_client.VocabulariesApi(api_client)

    try:
        # Récupération des statuts des collections de Nakala.
        api_response = api_instance.vocabularies_collection_statuses_get()
        print("The response of VocabulariesApi->vocabularies_collection_statuses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_collection_statuses_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des statuts de collections |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_country_codes_get**
> List[VocabulariesCountryCodesGet200ResponseInner] vocabularies_country_codes_get(q=q, code=code, order=order, page=page, limit=limit)

Récupération des codes pays ISO 3166 (alpha-2).

Retourne la liste des codes pays disponibles pour renseigner une métadonnée de type dcterms:ISO3166.
Cette liste correspond aux codes pays répertoriés par l'ISO 3166 (alpha-2).
La recherche et le tri sur le label des langues se fait en fonction de l'entête `Accept-Language` de la requête. L'anglais est la valeur par défaut.

### Example


```python
import openapi_client
from openapi_client.models.vocabularies_country_codes_get200_response_inner import VocabulariesCountryCodesGet200ResponseInner
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
    api_instance = openapi_client.VocabulariesApi(api_client)
    q = 'q_example' # str | Mot clé pour la recherche sur le code ou le label des pays (optional)
    code = 'code_example' # str | Code exact du pays recherché (optional)
    order = 'asc' # str | Sens du tri (basé sur le label des pays) (optional) (default to 'asc')
    page = '1' # str | Page courante (optional) (default to '1')
    limit = '10' # str | Nombre de résultats par page (optional) (default to '10')

    try:
        # Récupération des codes pays ISO 3166 (alpha-2).
        api_response = api_instance.vocabularies_country_codes_get(q=q, code=code, order=order, page=page, limit=limit)
        print("The response of VocabulariesApi->vocabularies_country_codes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_country_codes_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Mot clé pour la recherche sur le code ou le label des pays | [optional] 
 **code** | **str**| Code exact du pays recherché | [optional] 
 **order** | **str**| Sens du tri (basé sur le label des pays) | [optional] [default to &#39;asc&#39;]
 **page** | **str**| Page courante | [optional] [default to &#39;1&#39;]
 **limit** | **str**| Nombre de résultats par page | [optional] [default to &#39;10&#39;]

### Return type

[**List[VocabulariesCountryCodesGet200ResponseInner]**](VocabulariesCountryCodesGet200ResponseInner.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des pays disponibles |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_data_statuses_get**
> List[str] vocabularies_data_statuses_get()

Récupération des statuts des données de Nakala.

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
    api_instance = openapi_client.VocabulariesApi(api_client)

    try:
        # Récupération des statuts des données de Nakala.
        api_response = api_instance.vocabularies_data_statuses_get()
        print("The response of VocabulariesApi->vocabularies_data_statuses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_data_statuses_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des statuts de données |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_datatypes_get**
> List[str] vocabularies_datatypes_get()

Récupération des types des données de Nakala.

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
    api_instance = openapi_client.VocabulariesApi(api_client)

    try:
        # Récupération des types des données de Nakala.
        api_response = api_instance.vocabularies_datatypes_get()
        print("The response of VocabulariesApi->vocabularies_datatypes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_datatypes_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des types de données |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_dcmitypes_get**
> List[str] vocabularies_dcmitypes_get()

Récupération des types DCMI.

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
    api_instance = openapi_client.VocabulariesApi(api_client)

    try:
        # Récupération des types DCMI.
        api_response = api_instance.vocabularies_dcmitypes_get()
        print("The response of VocabulariesApi->vocabularies_dcmitypes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_dcmitypes_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des types DCMI |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_languages_get**
> List[VocabulariesLanguagesGet200ResponseInner] vocabularies_languages_get(q=q, code=code, order=order, page=page, limit=limit)

Récupération des langues des métadonnées.

Retourne la liste des langues disponibles pour déclarer la langue d'une métadonnée.
Cette liste correspond aux langues répertoriées par l'ISO-639-3.
Le code donné pour chaque langue correspond à celui de l'ISO-639-1 (sur deux caractères) lorsqu'il est disponible ou à celui l'ISO-639-3 dans le cas contraire.
La recherche et le tri sur le label des langues se fait en fonction de l'entête `Accept-Language` de la requête. L'anglais est la valeur par défaut.

### Example


```python
import openapi_client
from openapi_client.models.vocabularies_languages_get200_response_inner import VocabulariesLanguagesGet200ResponseInner
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
    api_instance = openapi_client.VocabulariesApi(api_client)
    q = 'q_example' # str | Mot clé pour la recherche sur le code ou le label des langues (optional)
    code = 'code_example' # str | Code exact de la langue recherchée (optional)
    order = 'asc' # str | Sens du tri (basé sur le label des langues) (optional) (default to 'asc')
    page = '1' # str | Page courante (optional) (default to '1')
    limit = '10' # str | Nombre de résultats par page (optional) (default to '10')

    try:
        # Récupération des langues des métadonnées.
        api_response = api_instance.vocabularies_languages_get(q=q, code=code, order=order, page=page, limit=limit)
        print("The response of VocabulariesApi->vocabularies_languages_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_languages_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Mot clé pour la recherche sur le code ou le label des langues | [optional] 
 **code** | **str**| Code exact de la langue recherchée | [optional] 
 **order** | **str**| Sens du tri (basé sur le label des langues) | [optional] [default to &#39;asc&#39;]
 **page** | **str**| Page courante | [optional] [default to &#39;1&#39;]
 **limit** | **str**| Nombre de résultats par page | [optional] [default to &#39;10&#39;]

### Return type

[**List[VocabulariesLanguagesGet200ResponseInner]**](VocabulariesLanguagesGet200ResponseInner.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des langues disponibles |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_licenses_get**
> List[License] vocabularies_licenses_get(q=q, code=code)

Récupération des licences des données de Nakala.

### Example


```python
import openapi_client
from openapi_client.models.license import License
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
    api_instance = openapi_client.VocabulariesApi(api_client)
    q = 'q_example' # str | Mot clé pour la recherche sur le code ou le nom des licences (optional)
    code = 'code_example' # str | Code exact de la licence recherchée (optional)

    try:
        # Récupération des licences des données de Nakala.
        api_response = api_instance.vocabularies_licenses_get(q=q, code=code)
        print("The response of VocabulariesApi->vocabularies_licenses_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_licenses_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Mot clé pour la recherche sur le code ou le nom des licences | [optional] 
 **code** | **str**| Code exact de la licence recherchée | [optional] 

### Return type

[**List[License]**](License.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des licences |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_metadatatypes_get**
> List[str] vocabularies_metadatatypes_get()

Récupération des types des métadonnées.

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
    api_instance = openapi_client.VocabulariesApi(api_client)

    try:
        # Récupération des types des métadonnées.
        api_response = api_instance.vocabularies_metadatatypes_get()
        print("The response of VocabulariesApi->vocabularies_metadatatypes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_metadatatypes_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des types des métadonnées |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vocabularies_properties_get**
> List[str] vocabularies_properties_get()

Récupération des propriétés des métadonnées.

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
    api_instance = openapi_client.VocabulariesApi(api_client)

    try:
        # Récupération des propriétés des métadonnées.
        api_response = api_instance.vocabularies_properties_get()
        print("The response of VocabulariesApi->vocabularies_properties_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling VocabulariesApi->vocabularies_properties_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**List[str]**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Liste des propriétés des métadonnées |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

