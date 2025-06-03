# Data4


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **int** | Numéro de version de la donnée | [optional] 
**files** | [**List[File2]**](File2.md) |  | [optional] 
**last_moderator** | **object** |  | [optional] 
**last_moderation_date** | **datetime** |  | [optional] 
**relations** | [**List[Relation]**](Relation.md) |  | [optional] 
**status** | **str** |  | [optional] 
**file_embargoed** | **bool** |  | [optional] 
**uri** | **str** |  | [optional] 
**identifier** | **str** |  | [optional] 
**metas** | [**List[Meta2]**](Meta2.md) |  | [optional] 

## Example

```python
from openapi_client.models.data4 import Data4

# TODO update the JSON string below
json = "{}"
# create an instance of Data4 from a JSON string
data4_instance = Data4.from_json(json)
# print the JSON string representation of the object
print(Data4.to_json())

# convert the object into a dict
data4_dict = data4_instance.to_dict()
# create an instance of Data4 from a dict
data4_from_dict = Data4.from_dict(data4_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


