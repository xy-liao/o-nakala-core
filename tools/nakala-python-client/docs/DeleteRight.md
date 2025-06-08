# DeleteRight

Droit à supprimer

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Uuid d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**role** | [**Role**](Role.md) |  | [optional] 

## Example

```python
from openapi_client.models.delete_right import DeleteRight

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteRight from a JSON string
delete_right_instance = DeleteRight.from_json(json)
# print the JSON string representation of the object
print(DeleteRight.to_json())

# convert the object into a dict
delete_right_dict = delete_right_instance.to_dict()
# create an instance of DeleteRight from a dict
delete_right_from_dict = DeleteRight.from_dict(delete_right_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


