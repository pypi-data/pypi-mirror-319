# CreateConfirmDeliveryDetailsRequest

The request schema for the createConfirmDeliveryDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The text to be sent to the buyer. Only links related to order delivery are allowed. Do not include HTML or email addresses. The text must be written in the buyer&#39;s language of preference, which can be retrieved from the GetAttributes operation. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_confirm_delivery_details_request import CreateConfirmDeliveryDetailsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConfirmDeliveryDetailsRequest from a JSON string
create_confirm_delivery_details_request_instance = CreateConfirmDeliveryDetailsRequest.from_json(json)
# print the JSON string representation of the object
print(CreateConfirmDeliveryDetailsRequest.to_json())

# convert the object into a dict
create_confirm_delivery_details_request_dict = create_confirm_delivery_details_request_instance.to_dict()
# create an instance of CreateConfirmDeliveryDetailsRequest from a dict
create_confirm_delivery_details_request_from_dict = CreateConfirmDeliveryDetailsRequest.from_dict(create_confirm_delivery_details_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


