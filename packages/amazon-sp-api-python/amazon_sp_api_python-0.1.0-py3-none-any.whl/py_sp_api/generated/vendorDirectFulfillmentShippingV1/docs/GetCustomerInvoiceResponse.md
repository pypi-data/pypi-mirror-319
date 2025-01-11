# GetCustomerInvoiceResponse

The response schema for the getCustomerInvoice operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CustomerInvoice**](CustomerInvoice.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_customer_invoice_response import GetCustomerInvoiceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCustomerInvoiceResponse from a JSON string
get_customer_invoice_response_instance = GetCustomerInvoiceResponse.from_json(json)
# print the JSON string representation of the object
print(GetCustomerInvoiceResponse.to_json())

# convert the object into a dict
get_customer_invoice_response_dict = get_customer_invoice_response_instance.to_dict()
# create an instance of GetCustomerInvoiceResponse from a dict
get_customer_invoice_response_from_dict = GetCustomerInvoiceResponse.from_dict(get_customer_invoice_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


