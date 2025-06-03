# User5


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** |  | [optional] 
**givenname** | **str** |  | [optional] 
**surname** | **str** |  | [optional] 
**photo** | **bytearray** |  | [optional] 
**fullname** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.user5 import User5

# TODO update the JSON string below
json = "{}"
# create an instance of User5 from a JSON string
user5_instance = User5.from_json(json)
# print the JSON string representation of the object
print(User5.to_json())

# convert the object into a dict
user5_dict = user5_instance.to_dict()
# create an instance of User5 from a dict
user5_from_dict = User5.from_dict(user5_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


