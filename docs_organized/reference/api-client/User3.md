# User3


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
from openapi_client.models.user3 import User3

# TODO update the JSON string below
json = "{}"
# create an instance of User3 from a JSON string
user3_instance = User3.from_json(json)
# print the JSON string representation of the object
print(User3.to_json())

# convert the object into a dict
user3_dict = user3_instance.to_dict()
# create an instance of User3 from a dict
user3_from_dict = User3.from_dict(user3_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


