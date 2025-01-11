# GetCustomerInvoicesResponse

The response schema for the getCustomerInvoices operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CustomerInvoiceList**](CustomerInvoiceList.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.get_customer_invoices_response import GetCustomerInvoicesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetCustomerInvoicesResponse from a JSON string
get_customer_invoices_response_instance = GetCustomerInvoicesResponse.from_json(json)
# print the JSON string representation of the object
print(GetCustomerInvoicesResponse.to_json())

# convert the object into a dict
get_customer_invoices_response_dict = get_customer_invoices_response_instance.to_dict()
# create an instance of GetCustomerInvoicesResponse from a dict
get_customer_invoices_response_from_dict = GetCustomerInvoicesResponse.from_dict(get_customer_invoices_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


