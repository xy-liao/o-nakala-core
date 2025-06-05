# File2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | un nom de fichier | [optional] 
**extension** | **str** |  | [optional] 
**size** | **str** |  | [optional] 
**sha1** | **str** |  | [optional] 
**embargoed** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**human_readable_embargoed_delay** | **List[int]** | Pattern représentant le temps restant d&#39;embargo en année (y) mois (m) et jour (d) | [optional] 
**puid** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.file2 import File2

# TODO update the JSON string below
json = "{}"
# create an instance of File2 from a JSON string
file2_instance = File2.from_json(json)
# print the JSON string representation of the object
print(File2.to_json())

# convert the object into a dict
file2_dict = file2_instance.to_dict()
# create an instance of File2 from a dict
file2_from_dict = File2.from_dict(file2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


