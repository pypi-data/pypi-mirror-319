# CustomerInvoiceList

Represents a list of customer invoices, potentially paginated.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**customer_invoices** | [**List[CustomerInvoice]**](CustomerInvoice.md) | Represents a customer invoice within the CustomerInvoiceList. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.customer_invoice_list import CustomerInvoiceList

# TODO update the JSON string below
json = "{}"
# create an instance of CustomerInvoiceList from a JSON string
customer_invoice_list_instance = CustomerInvoiceList.from_json(json)
# print the JSON string representation of the object
print(CustomerInvoiceList.to_json())

# convert the object into a dict
customer_invoice_list_dict = customer_invoice_list_instance.to_dict()
# create an instance of CustomerInvoiceList from a dict
customer_invoice_list_from_dict = CustomerInvoiceList.from_dict(customer_invoice_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


