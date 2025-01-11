# EventBridgeResourceSpecification

The information required to create an Amazon EventBridge destination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**region** | **str** | The AWS region in which you will be receiving the notifications. | 
**account_id** | **str** | The identifier for the AWS account that is responsible for charges related to receiving notifications. | 

## Example

```python
from py_sp_api.generated.notifications.models.event_bridge_resource_specification import EventBridgeResourceSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of EventBridgeResourceSpecification from a JSON string
event_bridge_resource_specification_instance = EventBridgeResourceSpecification.from_json(json)
# print the JSON string representation of the object
print(EventBridgeResourceSpecification.to_json())

# convert the object into a dict
event_bridge_resource_specification_dict = event_bridge_resource_specification_instance.to_dict()
# create an instance of EventBridgeResourceSpecification from a dict
event_bridge_resource_specification_from_dict = EventBridgeResourceSpecification.from_dict(event_bridge_resource_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


