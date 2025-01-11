# DestinationResource

The destination resource types.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sqs** | [**SqsResource**](SqsResource.md) |  | [optional] 
**event_bridge** | [**EventBridgeResource**](EventBridgeResource.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.destination_resource import DestinationResource

# TODO update the JSON string below
json = "{}"
# create an instance of DestinationResource from a JSON string
destination_resource_instance = DestinationResource.from_json(json)
# print the JSON string representation of the object
print(DestinationResource.to_json())

# convert the object into a dict
destination_resource_dict = destination_resource_instance.to_dict()
# create an instance of DestinationResource from a dict
destination_resource_from_dict = DestinationResource.from_dict(destination_resource_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


