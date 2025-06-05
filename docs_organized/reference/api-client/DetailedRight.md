# DetailedRight

Droit sur une resource de NAKALA

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Uuid d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**username** | **str** | Username d&#39;un utilisateur | [optional] 
**photo** | **str** | Photo de profil d&#39;un utilisateur | [optional] 
**name** | **str** | Nom d&#39;un groupe ou d&#39;un utilisateur | [optional] 
**users** | [**List[UserInfo]**](UserInfo.md) | Liste des utilisateurs appartenant au groupe | [optional] 
**role** | [**Role**](Role.md) |  | [optional] 
**type** | **str** | Type de groupe | [optional] 

## Example

```python
from openapi_client.models.detailed_right import DetailedRight

# TODO update the JSON string below
json = "{}"
# create an instance of DetailedRight from a JSON string
detailed_right_instance = DetailedRight.from_json(json)
# print the JSON string representation of the object
print(DetailedRight.to_json())

# convert the object into a dict
detailed_right_dict = detailed_right_instance.to_dict()
# create an instance of DetailedRight from a dict
detailed_right_from_dict = DetailedRight.from_dict(detailed_right_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


