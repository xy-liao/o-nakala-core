# User


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** |  | [optional] 
**givenname** | **str** |  | [optional] 
**surname** | **str** |  | [optional] 
**mail** | **str** |  | [optional] 
**photo** | **bytearray** |  | [optional] 
**first_login** | **datetime** |  | [optional] 
**last_login** | **datetime** |  | [optional] 
**roles** | **List[str]** |  | [optional] 
**api_key** | **str** |  | [optional] 
**fullname** | **str** |  | [optional] 
**user_group_id** | **str** | Identifiant interne de l&#39;utilisateur | [optional] 

## Example

```python
from openapi_client.models.user import User

# TODO update the JSON string below
json = "{}"
# create an instance of User from a JSON string
user_instance = User.from_json(json)
# print the JSON string representation of the object
print(User.to_json())

# convert the object into a dict
user_dict = user_instance.to_dict()
# create an instance of User from a dict
user_from_dict = User.from_dict(user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


