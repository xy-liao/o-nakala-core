# File5


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | un nom de fichier | [optional] 
**sha1** | **str** |  | [optional] 
**embargoed** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.file5 import File5

# TODO update the JSON string below
json = "{}"
# create an instance of File5 from a JSON string
file5_instance = File5.from_json(json)
# print the JSON string representation of the object
print(File5.to_json())

# convert the object into a dict
file5_dict = file5_instance.to_dict()
# create an instance of File5 from a dict
file5_from_dict = File5.from_dict(file5_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


