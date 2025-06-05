# DetailedAbstractGroup

Utilisateur ou groupe d'utilisateurs

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Uuid d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**username** | **str** | Username d&#39;un utilisateur | [optional] 
**photo** | **str** | Photo de profil d&#39;un utilisateur | [optional] 
**name** | **str** | Nom d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**users** | [**List[UserInfo]**](UserInfo.md) | Liste des utilisateurs appartenant au groupe | [optional] 
**type** | **str** | Type de groupe | [optional] 
**datemodify** | **date** | Date de création ou dernière date de modification du groupe | [optional] 
**is_owner** | **bool** | L&#39;utilisateur connecté est le propriétaire du groupe | [optional] 
**is_admin** | **bool** | L&#39;utilisateur connecté fait parti des administrateurs du groupe | [optional] 
**is_member** | **bool** | L&#39;utilisteur connecté fait parti des membres du groupe | [optional] 

## Example

```python
from openapi_client.models.detailed_abstract_group import DetailedAbstractGroup

# TODO update the JSON string below
json = "{}"
# create an instance of DetailedAbstractGroup from a JSON string
detailed_abstract_group_instance = DetailedAbstractGroup.from_json(json)
# print the JSON string representation of the object
print(DetailedAbstractGroup.to_json())

# convert the object into a dict
detailed_abstract_group_dict = detailed_abstract_group_instance.to_dict()
# create an instance of DetailedAbstractGroup from a dict
detailed_abstract_group_from_dict = DetailedAbstractGroup.from_dict(detailed_abstract_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


