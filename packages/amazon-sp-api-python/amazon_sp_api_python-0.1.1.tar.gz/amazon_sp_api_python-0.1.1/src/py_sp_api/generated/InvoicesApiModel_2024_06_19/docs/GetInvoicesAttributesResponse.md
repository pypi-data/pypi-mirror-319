# GetInvoicesAttributesResponse

Success.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoices_attributes** | [**InvoicesAttributes**](InvoicesAttributes.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.get_invoices_attributes_response import GetInvoicesAttributesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetInvoicesAttributesResponse from a JSON string
get_invoices_attributes_response_instance = GetInvoicesAttributesResponse.from_json(json)
# print the JSON string representation of the object
print(GetInvoicesAttributesResponse.to_json())

# convert the object into a dict
get_invoices_attributes_response_dict = get_invoices_attributes_response_instance.to_dict()
# create an instance of GetInvoicesAttributesResponse from a dict
get_invoices_attributes_response_from_dict = GetInvoicesAttributesResponse.from_dict(get_invoices_attributes_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


