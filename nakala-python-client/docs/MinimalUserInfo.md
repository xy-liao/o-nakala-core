# MinimalUserInfo

Information minimum sur un utilisateur

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**username** | **str** | Username d&#39;un utilisateur | [optional] 
**role** | **str** | Role de l&#39;utilisateur sur la gestion du groupe | [optional] 

## Example

```python
from openapi_client.models.minimal_user_info import MinimalUserInfo

# TODO update the JSON string below
json = "{}"
# create an instance of MinimalUserInfo from a JSON string
minimal_user_info_instance = MinimalUserInfo.from_json(json)
# print the JSON string representation of the object
print(MinimalUserInfo.to_json())

# convert the object into a dict
minimal_user_info_dict = minimal_user_info_instance.to_dict()
# create an instance of MinimalUserInfo from a dict
minimal_user_info_from_dict = MinimalUserInfo.from_dict(minimal_user_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


