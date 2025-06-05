# User2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**givenname** | **str** |  | [optional] 
**surname** | **str** |  | [optional] 
**mail** | **str** |  | [optional] 
**photo** | **bytearray** |  | [optional] 

## Example

```python
from openapi_client.models.user2 import User2

# TODO update the JSON string below
json = "{}"
# create an instance of User2 from a JSON string
user2_instance = User2.from_json(json)
# print the JSON string representation of the object
print(User2.to_json())

# convert the object into a dict
user2_dict = user2_instance.to_dict()
# create an instance of User2 from a dict
user2_from_dict = User2.from_dict(user2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


