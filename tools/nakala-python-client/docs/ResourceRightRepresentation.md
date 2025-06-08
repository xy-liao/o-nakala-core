# ResourceRightRepresentation

Le droit : id du groupe et role

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**role** | [**Role**](Role.md) |  | [optional] 

## Example

```python
from openapi_client.models.resource_right_representation import ResourceRightRepresentation

# TODO update the JSON string below
json = "{}"
# create an instance of ResourceRightRepresentation from a JSON string
resource_right_representation_instance = ResourceRightRepresentation.from_json(json)
# print the JSON string representation of the object
print(ResourceRightRepresentation.to_json())

# convert the object into a dict
resource_right_representation_dict = resource_right_representation_instance.to_dict()
# create an instance of ResourceRightRepresentation from a dict
resource_right_representation_from_dict = ResourceRightRepresentation.from_dict(resource_right_representation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


