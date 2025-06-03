# File4


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
from openapi_client.models.file4 import File4

# TODO update the JSON string below
json = "{}"
# create an instance of File4 from a JSON string
file4_instance = File4.from_json(json)
# print the JSON string representation of the object
print(File4.to_json())

# convert the object into a dict
file4_dict = file4_instance.to_dict()
# create an instance of File4 from a dict
file4_from_dict = File4.from_dict(file4_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


