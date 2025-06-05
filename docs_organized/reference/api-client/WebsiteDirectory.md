# WebsiteDirectory


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**prefix** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**updated_at** | **datetime** |  | [optional] 
**title** | [**List[TitleInner]**](TitleInner.md) |  | [optional] 
**description** | [**List[TitleInner]**](TitleInner.md) |  | [optional] 

## Example

```python
from openapi_client.models.website_directory import WebsiteDirectory

# TODO update the JSON string below
json = "{}"
# create an instance of WebsiteDirectory from a JSON string
website_directory_instance = WebsiteDirectory.from_json(json)
# print the JSON string representation of the object
print(WebsiteDirectory.to_json())

# convert the object into a dict
website_directory_dict = website_directory_instance.to_dict()
# create an instance of WebsiteDirectory from a dict
website_directory_from_dict = WebsiteDirectory.from_dict(website_directory_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


