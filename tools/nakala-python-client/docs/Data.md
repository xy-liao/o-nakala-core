# Data


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**version** | **int** | Numéro de version de la donnée | [optional] 
**collections_ids** | **str** |  | [optional] 
**files** | [**List[File4]**](File4.md) |  | [optional] 
**last_moderator** | [**User3**](User3.md) |  | [optional] 
**last_moderation_date** | **datetime** |  | [optional] 
**relations** | [**List[Relation3]**](Relation3.md) |  | [optional] 
**status** | **str** |  | [optional] 
**file_embargoed** | **bool** |  | [optional] 
**uri** | **str** |  | [optional] 
**identifier** | **str** |  | [optional] 
**handle_identifier** | **str** |  | [optional] 
**metas** | [**List[Meta4]**](Meta4.md) |  | [optional] 
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
from openapi_client.models.data import Data

# TODO update the JSON string below
json = "{}"
# create an instance of Data from a JSON string
data_instance = Data.from_json(json)
# print the JSON string representation of the object
print(Data.to_json())

# convert the object into a dict
data_dict = data_instance.to_dict()
# create an instance of Data from a dict
data_from_dict = Data.from_dict(data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


