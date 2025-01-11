# EventBridgeResource

The Amazon EventBridge destination.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The name of the partner event source associated with the destination. | 
**region** | **str** | The AWS region in which you receive the notifications. For AWS regions that are supported in Amazon EventBridge, refer to [Amazon EventBridge endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/ev.html). | 
**account_id** | **str** | The identifier for the AWS account that is responsible for charges related to receiving notifications. | 

## Example

```python
from py_sp_api.generated.notifications.models.event_bridge_resource import EventBridgeResource

# TODO update the JSON string below
json = "{}"
# create an instance of EventBridgeResource from a JSON string
event_bridge_resource_instance = EventBridgeResource.from_json(json)
# print the JSON string representation of the object
print(EventBridgeResource.to_json())

# convert the object into a dict
event_bridge_resource_dict = event_bridge_resource_instance.to_dict()
# create an instance of EventBridgeResource from a dict
event_bridge_resource_from_dict = EventBridgeResource.from_dict(event_bridge_resource_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


