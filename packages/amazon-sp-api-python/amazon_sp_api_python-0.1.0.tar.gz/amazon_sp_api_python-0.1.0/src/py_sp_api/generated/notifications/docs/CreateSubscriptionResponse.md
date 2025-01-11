# CreateSubscriptionResponse

The response schema for the `createSubscription` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**Subscription**](Subscription.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.create_subscription_response import CreateSubscriptionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateSubscriptionResponse from a JSON string
create_subscription_response_instance = CreateSubscriptionResponse.from_json(json)
# print the JSON string representation of the object
print(CreateSubscriptionResponse.to_json())

# convert the object into a dict
create_subscription_response_dict = create_subscription_response_instance.to_dict()
# create an instance of CreateSubscriptionResponse from a dict
create_subscription_response_from_dict = CreateSubscriptionResponse.from_dict(create_subscription_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


