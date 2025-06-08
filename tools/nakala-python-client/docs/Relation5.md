# Relation5


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Le type de relation | [optional] 
**repository** | **str** | Le nom de l&#39;entrepôt cible | [optional] 
**target** | **str** | L&#39;identifiant de la ressource cible | [optional] 
**var_date** | **datetime** |  | [optional] 
**comment** | **str** |  | [optional] 
**uri** | **str** | L&#39;URI vers la ressource cible | [optional] 
**is_inferred** | **bool** | Indique si la relation a été ajoutée par inférence | [optional] 

## Example

```python
from openapi_client.models.relation5 import Relation5

# TODO update the JSON string below
json = "{}"
# create an instance of Relation5 from a JSON string
relation5_instance = Relation5.from_json(json)
# print the JSON string representation of the object
print(Relation5.to_json())

# convert the object into a dict
relation5_dict = relation5_instance.to_dict()
# create an instance of Relation5 from a dict
relation5_from_dict = Relation5.from_dict(relation5_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


