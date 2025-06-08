# UserDatasQuery

Requête sur les données d'un utilisateur

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | **int** | La page souhaitée | [optional] [default to 1]
**limit** | **int** | Le nombre de résultats par page | [optional] 
**orders** | **List[str]** | La liste des tri souhaités | [optional] 
**types** | **List[str]** | URI des types recherchés | [optional] 
**status** | **List[str]** | Un ou plusieurs statut pour la donnée: pending, published, embargoed | [optional] 
**created_years** | **List[int]** | Liste des années de création recherchée | [optional] 
**collections** | **List[str]** | Liste des collections associées aux données recherchées | [optional] 
**title_search** | **str** |  | [optional] 
**title_search_lang** | **str** | Le code de langue (format ISO 639-1) pour la recherche textuelle dans le titre (titleSearch) | [optional] 
**order_lang** | **str** | Le code de langue (format ISO 639-1) pour l&#39;ordre des données indiqué par orders | [optional] [default to 'fr']

## Example

```python
from openapi_client.models.user_datas_query import UserDatasQuery

# TODO update the JSON string below
json = "{}"
# create an instance of UserDatasQuery from a JSON string
user_datas_query_instance = UserDatasQuery.from_json(json)
# print the JSON string representation of the object
print(UserDatasQuery.to_json())

# convert the object into a dict
user_datas_query_dict = user_datas_query_instance.to_dict()
# create an instance of UserDatasQuery from a dict
user_datas_query_from_dict = UserDatasQuery.from_dict(user_datas_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


