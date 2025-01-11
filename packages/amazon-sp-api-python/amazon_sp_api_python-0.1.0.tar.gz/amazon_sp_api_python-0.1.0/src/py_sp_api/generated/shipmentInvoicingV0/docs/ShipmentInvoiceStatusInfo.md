# ShipmentInvoiceStatusInfo

The shipment invoice status information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_shipment_id** | **str** | The Amazon-defined shipment identifier. | [optional] 
**invoice_status** | [**ShipmentInvoiceStatus**](ShipmentInvoiceStatus.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.shipment_invoice_status_info import ShipmentInvoiceStatusInfo

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentInvoiceStatusInfo from a JSON string
shipment_invoice_status_info_instance = ShipmentInvoiceStatusInfo.from_json(json)
# print the JSON string representation of the object
print(ShipmentInvoiceStatusInfo.to_json())

# convert the object into a dict
shipment_invoice_status_info_dict = shipment_invoice_status_info_instance.to_dict()
# create an instance of ShipmentInvoiceStatusInfo from a dict
shipment_invoice_status_info_from_dict = ShipmentInvoiceStatusInfo.from_dict(shipment_invoice_status_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


