# DestinationResourceSpecification

The information required to create a destination resource. Applications should use one resource type (sqs or eventBridge) per destination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sqs** | [**SqsResource**](SqsResource.md) |  | [optional] 
**event_bridge** | [**EventBridgeResourceSpecification**](EventBridgeResourceSpecification.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.destination_resource_specification import DestinationResourceSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of DestinationResourceSpecification from a JSON string
destination_resource_specification_instance = DestinationResourceSpecification.from_json(json)
# print the JSON string representation of the object
print(DestinationResourceSpecification.to_json())

# convert the object into a dict
destination_resource_specification_dict = destination_resource_specification_instance.to_dict()
# create an instance of DestinationResourceSpecification from a dict
destination_resource_specification_from_dict = DestinationResourceSpecification.from_dict(destination_resource_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


