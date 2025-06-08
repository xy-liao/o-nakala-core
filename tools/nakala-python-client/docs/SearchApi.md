# openapi_client.SearchApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**authors_search_get**](SearchApi.md#authors_search_get) | **GET** /authors/search | Récupération des auteurs associés aux données de Nakala.
[**search_get**](SearchApi.md#search_get) | **GET** /search | Recherche des données Nakala.


# **authors_search_get**
> List[Author] authors_search_get(q=q, order=order, page=page, limit=limit, search_operator=search_operator, search_field=search_field)

Récupération des auteurs associés aux données de Nakala.

Retourne des auteurs associés aux données de Nakala en fonction de critères de recherche

### Example


```python
import openapi_client
from openapi_client.models.author import Author
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
    api_instance = openapi_client.SearchApi(api_client)
    q = 'q_example' # str | Mot clé pour la recherche (optional)
    order = 'asc' # str | Sens du tri (basé le prénom puis le nom de famille) (optional) (default to 'asc')
    page = '1' # str | Page courante (optional) (default to '1')
    limit = '10' # str | Nombre de résultats par page (optional) (default to '10')
    search_operator = 'partial' # str | Permet de selectionner la recherche en début, fin ou contenu dans l'élément (start, end, partial(default)) (optional) (default to 'partial')
    search_field = 'all' # str | Permet de sélectionner le champ de recherche (surname, givenname, orcid, all(default)) (optional) (default to 'all')

    try:
        # Récupération des auteurs associés aux données de Nakala.
        api_response = api_instance.authors_search_get(q=q, order=order, page=page, limit=limit, search_operator=search_operator, search_field=search_field)
        print("The response of SearchApi->authors_search_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SearchApi->authors_search_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Mot clé pour la recherche | [optional] 
 **order** | **str**| Sens du tri (basé le prénom puis le nom de famille) | [optional] [default to &#39;asc&#39;]
 **page** | **str**| Page courante | [optional] [default to &#39;1&#39;]
 **limit** | **str**| Nombre de résultats par page | [optional] [default to &#39;10&#39;]
 **search_operator** | **str**| Permet de selectionner la recherche en début, fin ou contenu dans l&#39;élément (start, end, partial(default)) | [optional] [default to &#39;partial&#39;]
 **search_field** | **str**| Permet de sélectionner le champ de recherche (surname, givenname, orcid, all(default)) | [optional] [default to &#39;all&#39;]

### Return type

[**List[Author]**](Author.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retourne une liste d&#39;auteurs |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_get**
> search_get(q=q, fq=fq, facet=facet, order=order, page=page, size=size)

Recherche des données Nakala.

Retourne des données Nakala en fonction de critères de recherche
- `q` : requête à effectuer
- `fq` : filtres pour la requête
     - Filtres disponibles : scope, status, type, year, created<sup>1</sup>, modified<sup>1</sup> language, keyword, collection, license, fileExt, depositor, owner et share
     - Il est possible de rechercher sur plusieurs filtres ; le caractère de séparation est le point-virgule. La recherche est traduite par un ET entre les filtres.
     - Il est possible d'ajouter plusieurs valeurs pour un même filtre ; le caractère de séparation est la virgule ou le &. La recherche se fera par un OU entre les
valeurs dans le cas de la virgule et par un ET dans le cas du &. Il n'est pas possible de mélanger ces deux opérateurs pour un même filtre.
     - Exemple : scope=collection;status=public;year=2009,1889
- `facet` : facette(s) à retourner
     - Facettes disponibles : scope, status, type, year, created, license, language, keyword, fileExt, fileSize, fileType et collection
     - Il est possible de retourner plusieurs facettes ; le caractère de séparation est le point-virgule.
     - Il est possible de configurer la taille et l'ordre d'une facette avec les paramètres size, sort et order
     - Pour la facette created, size correspond au format date souhaité : yyyy, yyyy-MM ou yyyy-MM-dd
     - Exemple : type,size=17,sort=item,order=asc;fileExt,size=7,sort=count,order=desc
- `order` : tri des résultats
     - Valeurs possibles : relevance ou date,desc ou date,asc ou title,desc ou title,asc

1 : Spécificités du filtre `created` et `modified` :
- Les opérateurs suivants sont disponibles : `=`, `>`, `<`, `>=` et `<=`
- Le format complet est `YYYY-MM-DDT00:00:00`
- Les formats incomplets `YYYY` `YYYY-MM` et `YYYY-MM-DD` peuvent être utilisés. La recherche se traduira selon les règles suivantes :
     - pour l'opérateur `=` : la recherche se fera dans une période, bornes incluses.
         - 2023 : entre `2023-01-01T00:00:00` et `2023-12-31T23:59:59`
         - 2023-05 : entre `2023-05-01T00:00:00` et `2023-05-31T23:59:59`
         - 2023-05-05 : entre `2023-05-05T00:00:00` et `2023-05-05T23:59:59`
     - pour les opérateurs `<` et `>=`, la date est complétée en se basant sur le début de journée. Exemple : `2013-05` deviendra `2013-05-01T00:00:00`
     - pour les opérateurs `>` et `<=`, la date est complétée en se basant sur la fin de journée. Exemple : `2013-05` deviendra `2013-05-01T23:59:59`

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
    api_instance = openapi_client.SearchApi(api_client)
    q = 'q_example' # str | Mot clé pour la recherche (optional)
    fq = 'fq_example' # str | Filtres pour la recherche (optional)
    facet = 'facet_example' # str | Facettes à créer au retour de la recherche (optional)
    order = 'relevance' # str | Tri (optional) (default to 'relevance')
    page = '1' # str | Page courante (optional) (default to '1')
    size = '25' # str | Nombre de résultats par page (optional) (default to '25')

    try:
        # Recherche des données Nakala.
        api_instance.search_get(q=q, fq=fq, facet=facet, order=order, page=page, size=size)
    except Exception as e:
        print("Exception when calling SearchApi->search_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **q** | **str**| Mot clé pour la recherche | [optional] 
 **fq** | **str**| Filtres pour la recherche | [optional] 
 **facet** | **str**| Facettes à créer au retour de la recherche | [optional] 
 **order** | **str**| Tri | [optional] [default to &#39;relevance&#39;]
 **page** | **str**| Page courante | [optional] [default to &#39;1&#39;]
 **size** | **str**| Nombre de résultats par page | [optional] [default to &#39;25&#39;]

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
**200** | Retourne une liste de données |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

