# Data5


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **int** | Numéro de version de la donnée | [optional] 
**collections_ids** | **str** |  | [optional] 
**files** | [**List[File6]**](File6.md) |  | [optional] 
**last_moderator** | [**User5**](User5.md) |  | [optional] 
**last_moderation_date** | **datetime** |  | [optional] 
**relations** | [**List[Relation5]**](Relation5.md) |  | [optional] 
**status** | **str** |  | [optional] 
**file_embargoed** | **bool** |  | [optional] 
**uri** | **str** |  | [optional] 
**identifier** | **str** |  | [optional] 
**handle_identifier** | **str** |  | [optional] 
**metas** | [**List[Meta9]**](Meta9.md) |  | [optional] 
**cre_date** | **datetime** |  | [optional] 
**depositor** | [**AbstractGroup**](AbstractGroup.md) |  | [optional] 
**owner** | [**AbstractGroup**](AbstractGroup.md) |  | [optional] 
**is_depositor** | **bool** |  | [optional] 
**is_owner** | **bool** |  | [optional] 
**is_admin** | **bool** |  | [optional] 
**is_editor** | **bool** |  | [optional] 
**mod_date** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.data5 import Data5

# TODO update the JSON string below
json = "{}"
# create an instance of Data5 from a JSON string
data5_instance = Data5.from_json(json)
# print the JSON string representation of the object
print(Data5.to_json())

# convert the object into a dict
data5_dict = data5_instance.to_dict()
# create an instance of Data5 from a dict
data5_from_dict = Data5.from_dict(data5_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


