# CreateSubscriptionRequest

The request schema for the `createSubscription` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload_version** | **str** | The version of the payload object to be used in the notification. | 
**destination_id** | **str** | The identifier for the destination where notifications will be delivered. | 
**processing_directive** | [**ProcessingDirective**](ProcessingDirective.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.create_subscription_request import CreateSubscriptionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSubscriptionRequest from a JSON string
create_subscription_request_instance = CreateSubscriptionRequest.from_json(json)
# print the JSON string representation of the object
print(CreateSubscriptionRequest.to_json())

# convert the object into a dict
create_subscription_request_dict = create_subscription_request_instance.to_dict()
# create an instance of CreateSubscriptionRequest from a dict
create_subscription_request_from_dict = CreateSubscriptionRequest.from_dict(create_subscription_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


