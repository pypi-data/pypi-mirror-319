# CustomerInvoice

Represents a customer invoice associated with a purchase order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | The purchase order number for this order. | 
**content** | **str** | The Base64encoded customer invoice. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.customer_invoice import CustomerInvoice

# TODO update the JSON string below
json = "{}"
# create an instance of CustomerInvoice from a JSON string
customer_invoice_instance = CustomerInvoice.from_json(json)
# print the JSON string representation of the object
print(CustomerInvoice.to_json())

# convert the object into a dict
customer_invoice_dict = customer_invoice_instance.to_dict()
# create an instance of CustomerInvoice from a dict
customer_invoice_from_dict = CustomerInvoice.from_dict(customer_invoice_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


