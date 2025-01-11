# DeleteSubscriptionByIdResponse

The response schema for the `deleteSubscriptionById` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.notifications.models.delete_subscription_by_id_response import DeleteSubscriptionByIdResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DeleteSubscriptionByIdResponse from a JSON string
delete_subscription_by_id_response_instance = DeleteSubscriptionByIdResponse.from_json(json)
# print the JSON string representation of the object
print(DeleteSubscriptionByIdResponse.to_json())

# convert the object into a dict
delete_subscription_by_id_response_dict = delete_subscription_by_id_response_instance.to_dict()
# create an instance of DeleteSubscriptionByIdResponse from a dict
delete_subscription_by_id_response_from_dict = DeleteSubscriptionByIdResponse.from_dict(delete_subscription_by_id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


