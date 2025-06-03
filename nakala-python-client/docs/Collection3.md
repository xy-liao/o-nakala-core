# Collection3


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | [optional] 
**website_enabled** | **bool** |  | [optional] 
**website_published** | **bool** |  | [optional] 
**website_prefix** | **str** |  | [optional] 
**have_data** | **bool** |  | [optional] 
**have_accessible_data** | **bool** |  | [optional] 
**uri** | **str** |  | [optional] 
**identifier** | **str** |  | [optional] 
**handle_identifier** | **str** |  | [optional] 
**metas** | [**List[Meta7]**](Meta7.md) |  | [optional] 
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
from openapi_client.models.collection3 import Collection3

# TODO update the JSON string below
json = "{}"
# create an instance of Collection3 from a JSON string
collection3_instance = Collection3.from_json(json)
# print the JSON string representation of the object
print(Collection3.to_json())

# convert the object into a dict
collection3_dict = collection3_instance.to_dict()
# create an instance of Collection3 from a dict
collection3_from_dict = Collection3.from_dict(collection3_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


