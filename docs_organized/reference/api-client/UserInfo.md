# UserInfo

Information sur un utilisateur

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** | Username d&#39;un utilisateur | [optional] 
**fullname** | **str** | Nom complet d&#39;un utilisateur | [optional] 
**photo** | **str** | Photo de profil d&#39;un utilisateur | [optional] 
**role** | **str** | Role de l&#39;utilisateur sur la gestion du groupe | [optional] 

## Example

```python
from openapi_client.models.user_info import UserInfo

# TODO update the JSON string below
json = "{}"
# create an instance of UserInfo from a JSON string
user_info_instance = UserInfo.from_json(json)
# print the JSON string representation of the object
print(UserInfo.to_json())

# convert the object into a dict
user_info_dict = user_info_instance.to_dict()
# create an instance of UserInfo from a dict
user_info_from_dict = UserInfo.from_dict(user_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


