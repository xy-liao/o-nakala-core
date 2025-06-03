# Collection2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | [optional] 
**uri** | **str** |  | [optional] 
**identifier** | **str** |  | [optional] 
**metas** | [**List[Meta6]**](Meta6.md) |  | [optional] 
**cre_date** | **datetime** |  | [optional] 
**mod_date** | **datetime** |  | [optional] 

## Example

```python
from openapi_client.models.collection2 import Collection2

# TODO update the JSON string below
json = "{}"
# create an instance of Collection2 from a JSON string
collection2_instance = Collection2.from_json(json)
# print the JSON string representation of the object
print(Collection2.to_json())

# convert the object into a dict
collection2_dict = collection2_instance.to_dict()
# create an instance of Collection2 from a dict
collection2_from_dict = Collection2.from_dict(collection2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


