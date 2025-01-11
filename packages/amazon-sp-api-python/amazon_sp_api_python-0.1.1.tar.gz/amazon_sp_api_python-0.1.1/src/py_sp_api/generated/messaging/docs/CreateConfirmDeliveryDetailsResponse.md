# CreateConfirmDeliveryDetailsResponse

The response schema for the createConfirmDeliveryDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_confirm_delivery_details_response import CreateConfirmDeliveryDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConfirmDeliveryDetailsResponse from a JSON string
create_confirm_delivery_details_response_instance = CreateConfirmDeliveryDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(CreateConfirmDeliveryDetailsResponse.to_json())

# convert the object into a dict
create_confirm_delivery_details_response_dict = create_confirm_delivery_details_response_instance.to_dict()
# create an instance of CreateConfirmDeliveryDetailsResponse from a dict
create_confirm_delivery_details_response_from_dict = CreateConfirmDeliveryDetailsResponse.from_dict(create_confirm_delivery_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


