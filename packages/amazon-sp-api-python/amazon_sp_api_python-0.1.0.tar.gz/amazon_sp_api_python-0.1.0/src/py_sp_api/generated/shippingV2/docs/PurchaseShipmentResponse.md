# PurchaseShipmentResponse

The response schema for the purchaseShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**PurchaseShipmentResult**](PurchaseShipmentResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.purchase_shipment_response import PurchaseShipmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseShipmentResponse from a JSON string
purchase_shipment_response_instance = PurchaseShipmentResponse.from_json(json)
# print the JSON string representation of the object
print(PurchaseShipmentResponse.to_json())

# convert the object into a dict
purchase_shipment_response_dict = purchase_shipment_response_instance.to_dict()
# create an instance of PurchaseShipmentResponse from a dict
purchase_shipment_response_from_dict = PurchaseShipmentResponse.from_dict(purchase_shipment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


