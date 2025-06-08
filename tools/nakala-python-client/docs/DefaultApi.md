# openapi_client.DefaultApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**resourceprocessing_identifier_get**](DefaultApi.md#resourceprocessing_identifier_get) | **GET** /resourceprocessing/{identifier} | État d&#39;une ressource dans ElasticSearch et Datacite.


# **resourceprocessing_identifier_get**
> List[ResourceProcessing] resourceprocessing_identifier_get(identifier)

État d'une ressource dans ElasticSearch et Datacite.

Permet de connaître l'état d'une ressource (donnée ou collection) dans ElasticSearch et Datacite.

### Example


```python
import openapi_client
from openapi_client.models.resource_processing import ResourceProcessing
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
    api_instance = openapi_client.DefaultApi(api_client)
    identifier = 'identifier_example' # str | Identifiant de la ressource (donnée ou collection)

    try:
        # État d'une ressource dans ElasticSearch et Datacite.
        api_response = api_instance.resourceprocessing_identifier_get(identifier)
        print("The response of DefaultApi->resourceprocessing_identifier_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->resourceprocessing_identifier_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **identifier** | **str**| Identifiant de la ressource (donnée ou collection) | 

### Return type

[**List[ResourceProcessing]**](ResourceProcessing.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retourne l&#39;état d&#39;une ressource dans ElasticSearch et Datacite |  -  |
**404** | Aucune donnée ou collection trouvée dans ElasticSearch ou Datacite à partir de l&#39;identifiant fourni |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

