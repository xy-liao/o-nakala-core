# DatasIdentifierVersionsGet200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total** | **int** | Nombre de versions | [optional] 
**current_page** | **int** | Page courante | [optional] 
**last_page** | **int** | Dernière page disponible | [optional] 
**limit** | **int** | Nombre de versions par page | [optional] 
**data** | [**List[Data3]**](Data3.md) | Liste paginée des versions de la donnée | [optional] 

## Example

```python
from openapi_client.models.datas_identifier_versions_get200_response import DatasIdentifierVersionsGet200Response

# TODO update the JSON string below
json = "{}"
# create an instance of DatasIdentifierVersionsGet200Response from a JSON string
datas_identifier_versions_get200_response_instance = DatasIdentifierVersionsGet200Response.from_json(json)
# print the JSON string representation of the object
print(DatasIdentifierVersionsGet200Response.to_json())

# convert the object into a dict
datas_identifier_versions_get200_response_dict = datas_identifier_versions_get200_response_instance.to_dict()
# create an instance of DatasIdentifierVersionsGet200Response from a dict
datas_identifier_versions_get200_response_from_dict = DatasIdentifierVersionsGet200Response.from_dict(datas_identifier_versions_get200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


