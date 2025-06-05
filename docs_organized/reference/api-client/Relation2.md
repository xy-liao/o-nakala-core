# Relation2


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Le type de relation | [optional] 
**repository** | **str** | Le nom de l&#39;entrepôt cible | [optional] 
**target** | **str** | L&#39;identifiant de la ressource cible | [optional] 
**comment** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.relation2 import Relation2

# TODO update the JSON string below
json = "{}"
# create an instance of Relation2 from a JSON string
relation2_instance = Relation2.from_json(json)
# print the JSON string representation of the object
print(Relation2.to_json())

# convert the object into a dict
relation2_dict = relation2_instance.to_dict()
# create an instance of Relation2 from a dict
relation2_from_dict = Relation2.from_dict(relation2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


