# GetInvoiceStatusResponse

The response schema for the getInvoiceStatus operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ShipmentInvoiceStatusResponse**](ShipmentInvoiceStatusResponse.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.get_invoice_status_response import GetInvoiceStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetInvoiceStatusResponse from a JSON string
get_invoice_status_response_instance = GetInvoiceStatusResponse.from_json(json)
# print the JSON string representation of the object
print(GetInvoiceStatusResponse.to_json())

# convert the object into a dict
get_invoice_status_response_dict = get_invoice_status_response_instance.to_dict()
# create an instance of GetInvoiceStatusResponse from a dict
get_invoice_status_response_from_dict = GetInvoiceStatusResponse.from_dict(get_invoice_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


