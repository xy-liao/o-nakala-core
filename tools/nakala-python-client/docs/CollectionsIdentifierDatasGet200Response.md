# CollectionsIdentifierDatasGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Le nombre de données dans la collection | [optional] 
**current_page** | **int** | La page actuelle | [optional] 
**last_page** | **int** | Le nombre total de page | [optional] 
**limit** | **int** | Le nombre de donnée par page, 25 au maximum | [optional] 
**data** | [**List[Data4]**](Data4.md) |  | [optional] 

## Example

```python
from openapi_client.models.collections_identifier_datas_get200_response import CollectionsIdentifierDatasGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionsIdentifierDatasGet200Response from a JSON string
collections_identifier_datas_get200_response_instance = CollectionsIdentifierDatasGet200Response.from_json(json)
# print the JSON string representation of the object
print(CollectionsIdentifierDatasGet200Response.to_json())

# convert the object into a dict
collections_identifier_datas_get200_response_dict = collections_identifier_datas_get200_response_instance.to_dict()
# create an instance of CollectionsIdentifierDatasGet200Response from a dict
collections_identifier_datas_get200_response_from_dict = CollectionsIdentifierDatasGet200Response.from_dict(collections_identifier_datas_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


