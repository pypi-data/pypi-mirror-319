# SubmitShipmentConfirmationsRequest

The request schema for the submitShipmentConfirmations operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_confirmations** | [**List[ShipmentConfirmation]**](ShipmentConfirmation.md) | Array of ShipmentConfirmation objects, each representing confirmation details for a specific shipment. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.submit_shipment_confirmations_request import SubmitShipmentConfirmationsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SubmitShipmentConfirmationsRequest from a JSON string
submit_shipment_confirmations_request_instance = SubmitShipmentConfirmationsRequest.from_json(json)
# print the JSON string representation of the object
print(SubmitShipmentConfirmationsRequest.to_json())

# convert the object into a dict
submit_shipment_confirmations_request_dict = submit_shipment_confirmations_request_instance.to_dict()
# create an instance of SubmitShipmentConfirmationsRequest from a dict
submit_shipment_confirmations_request_from_dict = SubmitShipmentConfirmationsRequest.from_dict(submit_shipment_confirmations_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


