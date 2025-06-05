# AbstractGroup

Utilisateur ou groupe d'utilisateurs

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Uuid d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**username** | **str** | Username d&#39;un utilisateur | [optional] 
**surname** | **str** | Nom de famille d&#39;un utilisateur | [optional] 
**givenname** | **str** | Prénom d&#39;un utilisateur | [optional] 
**photo** | **str** | Photo de profil d&#39;un utilisateur | [optional] 
**name** | **str** | Nom d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**users** | [**List[UserInfo]**](UserInfo.md) | Liste des utilisateurs appartenant au groupe | [optional] 
**type** | **str** | Type de groupe | [optional] 

## Example

```python
from openapi_client.models.abstract_group import AbstractGroup

# TODO update the JSON string below
json = "{}"
# create an instance of AbstractGroup from a JSON string
abstract_group_instance = AbstractGroup.from_json(json)
# print the JSON string representation of the object
print(AbstractGroup.to_json())

# convert the object into a dict
abstract_group_dict = abstract_group_instance.to_dict()
# create an instance of AbstractGroup from a dict
abstract_group_from_dict = AbstractGroup.from_dict(abstract_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


