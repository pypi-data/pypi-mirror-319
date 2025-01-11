# ConfirmShipmentErrorResponse

The error response schema for the `confirmShipment` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.confirm_shipment_error_response import ConfirmShipmentErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmShipmentErrorResponse from a JSON string
confirm_shipment_error_response_instance = ConfirmShipmentErrorResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmShipmentErrorResponse.to_json())

# convert the object into a dict
confirm_shipment_error_response_dict = confirm_shipment_error_response_instance.to_dict()
# create an instance of ConfirmShipmentErrorResponse from a dict
confirm_shipment_error_response_from_dict = ConfirmShipmentErrorResponse.from_dict(confirm_shipment_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


