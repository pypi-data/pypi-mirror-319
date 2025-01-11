# InvoiceDetails

The invoice details for charges associated with the goods in the package. Only applies to certain regions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoice_number** | **str** | The invoice number of the item. | [optional] 
**invoice_date** | **datetime** | The invoice date of the item in ISO 8061 format. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.invoice_details import InvoiceDetails

# TODO update the JSON string below
json = "{}"
# create an instance of InvoiceDetails from a JSON string
invoice_details_instance = InvoiceDetails.from_json(json)
# print the JSON string representation of the object
print(InvoiceDetails.to_json())

# convert the object into a dict
invoice_details_dict = invoice_details_instance.to_dict()
# create an instance of InvoiceDetails from a dict
invoice_details_from_dict = InvoiceDetails.from_dict(invoice_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


