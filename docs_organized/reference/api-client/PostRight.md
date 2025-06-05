# PostRight

Nouveau droit à ajouter

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Uuid d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**role** | [**Role**](Role.md) |  | [optional] 

## Example

```python
from openapi_client.models.post_right import PostRight

# TODO update the JSON string below
json = "{}"
# create an instance of PostRight from a JSON string
post_right_instance = PostRight.from_json(json)
# print the JSON string representation of the object
print(PostRight.to_json())

# convert the object into a dict
post_right_dict = post_right_instance.to_dict()
# create an instance of PostRight from a dict
post_right_from_dict = PostRight.from_dict(post_right_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


