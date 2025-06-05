# ResourceProcessing


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service** | **str** |  | [optional] 
**action** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**datestamp** | **datetime** |  | [optional] 
**message** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.resource_processing import ResourceProcessing

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceProcessing from a JSON string
resource_processing_instance = ResourceProcessing.from_json(json)
# print the JSON string representation of the object
print(ResourceProcessing.to_json())

# convert the object into a dict
resource_processing_dict = resource_processing_instance.to_dict()
# create an instance of ResourceProcessing from a dict
resource_processing_from_dict = ResourceProcessing.from_dict(resource_processing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


