# UsersCollectionsScopePost200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_records** | **int** |  | [optional] 
**data** | [**List[Collection5]**](Collection5.md) |  | [optional] 

## Example

```python
from openapi_client.models.users_collections_scope_post200_response import UsersCollectionsScopePost200Response

# TODO update the JSON string below
json = "{}"
# create an instance of UsersCollectionsScopePost200Response from a JSON string
users_collections_scope_post200_response_instance = UsersCollectionsScopePost200Response.from_json(json)
# print the JSON string representation of the object
print(UsersCollectionsScopePost200Response.to_json())

# convert the object into a dict
users_collections_scope_post200_response_dict = users_collections_scope_post200_response_instance.to_dict()
# create an instance of UsersCollectionsScopePost200Response from a dict
users_collections_scope_post200_response_from_dict = UsersCollectionsScopePost200Response.from_dict(users_collections_scope_post200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


