# ShipmentInvoiceStatusResponse

The shipment invoice status response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipments** | [**ShipmentInvoiceStatusInfo**](ShipmentInvoiceStatusInfo.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.shipment_invoice_status_response import ShipmentInvoiceStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentInvoiceStatusResponse from a JSON string
shipment_invoice_status_response_instance = ShipmentInvoiceStatusResponse.from_json(json)
# print the JSON string representation of the object
print(ShipmentInvoiceStatusResponse.to_json())

# convert the object into a dict
shipment_invoice_status_response_dict = shipment_invoice_status_response_instance.to_dict()
# create an instance of ShipmentInvoiceStatusResponse from a dict
shipment_invoice_status_response_from_dict = ShipmentInvoiceStatusResponse.from_dict(shipment_invoice_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


