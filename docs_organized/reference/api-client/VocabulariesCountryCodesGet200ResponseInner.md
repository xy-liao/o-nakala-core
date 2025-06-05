# VocabulariesCountryCodesGet200ResponseInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | code du pays (ISO 3166 alpha-2) | [optional] 
**label** | **str** | nom du pays | [optional] 

## Example

```python
from openapi_client.models.vocabularies_country_codes_get200_response_inner import VocabulariesCountryCodesGet200ResponseInner

# TODO update the JSON string below
json = "{}"
# create an instance of VocabulariesCountryCodesGet200ResponseInner from a JSON string
vocabularies_country_codes_get200_response_inner_instance = VocabulariesCountryCodesGet200ResponseInner.from_json(json)
# print the JSON string representation of the object
print(VocabulariesCountryCodesGet200ResponseInner.to_json())

# convert the object into a dict
vocabularies_country_codes_get200_response_inner_dict = vocabularies_country_codes_get200_response_inner_instance.to_dict()
# create an instance of VocabulariesCountryCodesGet200ResponseInner from a dict
vocabularies_country_codes_get200_response_inner_from_dict = VocabulariesCountryCodesGet200ResponseInner.from_dict(vocabularies_country_codes_get200_response_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


