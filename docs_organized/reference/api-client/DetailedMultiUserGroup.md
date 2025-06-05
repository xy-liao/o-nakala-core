# DetailedMultiUserGroup

Groupe d'utilisateurs

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Uuid d&#39;un groupe d&#39;utilisateurs | [optional] 
**name** | **str** | Nom d&#39;un groupe | [optional] 
**users** | [**List[UserInfo]**](UserInfo.md) | Liste des utilisateurs appartenant au groupe | [optional] 
**datemodify** | **date** | Dernière date de modification du groupe | [optional] 
**is_owner** | **bool** | L&#39;utilisateur connecté est le propriétaire du groupe | [optional] 
**is_admin** | **bool** | L&#39;utilisateur connecté fait parti des administrateurs du groupe | [optional] 
**is_member** | **bool** | L&#39;utilisateur connecté fait parti des membres du groupe | [optional] 

## Example

```python
from openapi_client.models.detailed_multi_user_group import DetailedMultiUserGroup

# TODO update the JSON string below
json = "{}"
# create an instance of DetailedMultiUserGroup from a JSON string
detailed_multi_user_group_instance = DetailedMultiUserGroup.from_json(json)
# print the JSON string representation of the object
print(DetailedMultiUserGroup.to_json())

# convert the object into a dict
detailed_multi_user_group_dict = detailed_multi_user_group_instance.to_dict()
# create an instance of DetailedMultiUserGroup from a dict
detailed_multi_user_group_from_dict = DetailedMultiUserGroup.from_dict(detailed_multi_user_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


