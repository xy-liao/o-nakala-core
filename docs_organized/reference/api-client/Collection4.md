# Collection4


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** |  | [optional] 
**metas** | [**List[Meta8]**](Meta8.md) |  | [optional] 
**rights** | [**List[PostRight]**](PostRight.md) |  | [optional] 

## Example

```python
from openapi_client.models.collection4 import Collection4

# TODO update the JSON string below
json = "{}"
# create an instance of Collection4 from a JSON string
collection4_instance = Collection4.from_json(json)
# print the JSON string representation of the object
print(Collection4.to_json())

# convert the object into a dict
collection4_dict = collection4_instance.to_dict()
# create an instance of Collection4 from a dict
collection4_from_dict = Collection4.from_dict(collection4_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


