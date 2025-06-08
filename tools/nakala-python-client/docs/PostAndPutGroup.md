# PostAndPutGroup

Nouveau groupe à créer

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Nom du groupe | [optional] 
**users** | [**List[MinimalUserInfo]**](MinimalUserInfo.md) | Liste des utilisateurs appartenant au groupe avec leur rôle sur la gestion du groupe | [optional] 

## Example

```python
from openapi_client.models.post_and_put_group import PostAndPutGroup

# TODO update the JSON string below
json = "{}"
# create an instance of PostAndPutGroup from a JSON string
post_and_put_group_instance = PostAndPutGroup.from_json(json)
# print the JSON string representation of the object
print(PostAndPutGroup.to_json())

# convert the object into a dict
post_and_put_group_dict = post_and_put_group_instance.to_dict()
# create an instance of PostAndPutGroup from a dict
post_and_put_group_from_dict = PostAndPutGroup.from_dict(post_and_put_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


