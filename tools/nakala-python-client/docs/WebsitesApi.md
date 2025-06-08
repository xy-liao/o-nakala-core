# openapi_client.WebsitesApi

All URIs are relative to *http://apitest.nakala.fr*

Method | HTTP request | Description
------------- | ------------- | -------------
[**websites_get**](WebsitesApi.md#websites_get) | **GET** /websites | Renvoie les sites webs.


# **websites_get**
> List[WebsiteDirectory] websites_get()

Renvoie les sites webs.

### Example


```python
import openapi_client
from openapi_client.models.website_directory import WebsiteDirectory
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
    api_instance = openapi_client.WebsitesApi(api_client)

    try:
        # Renvoie les sites webs.
        api_response = api_instance.websites_get()
        print("The response of WebsitesApi->websites_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebsitesApi->websites_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[WebsiteDirectory]**](WebsiteDirectory.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retourne l&#39;objet Websites |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

