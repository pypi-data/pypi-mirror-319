# SubmitShipmentConfirmationsResponse

The response schema for the submitShipmentConfirmations operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**TransactionReference**](TransactionReference.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.submit_shipment_confirmations_response import SubmitShipmentConfirmationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitShipmentConfirmationsResponse from a JSON string
submit_shipment_confirmations_response_instance = SubmitShipmentConfirmationsResponse.from_json(json)
# print the JSON string representation of the object
print(SubmitShipmentConfirmationsResponse.to_json())

# convert the object into a dict
submit_shipment_confirmations_response_dict = submit_shipment_confirmations_response_instance.to_dict()
# create an instance of SubmitShipmentConfirmationsResponse from a dict
submit_shipment_confirmations_response_from_dict = SubmitShipmentConfirmationsResponse.from_dict(submit_shipment_confirmations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


