# Relation4


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Le type de relation | [optional] 
**repository** | **str** | Le nom de l&#39;entrepôt cible | [optional] 
**target** | **str** | L&#39;identifiant de la ressource cible | [optional] 
**comment** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.relation4 import Relation4

# TODO update the JSON string below
json = "{}"
# create an instance of Relation4 from a JSON string
relation4_instance = Relation4.from_json(json)
# print the JSON string representation of the object
print(Relation4.to_json())

# convert the object into a dict
relation4_dict = relation4_instance.to_dict()
# create an instance of Relation4 from a dict
relation4_from_dict = Relation4.from_dict(relation4_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


