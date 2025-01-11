# GetInvoicesExportsResponse

Success.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exports** | [**List[Export]**](Export.md) | A list of exports. | [optional] 
**next_token** | **str** | This token is returned when the number of results exceeds the specified &#x60;pageSize&#x60; value. To get the next page of results, call the &#x60;getInvoices&#x60; operation and include this token with the previous call parameters. | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.get_invoices_exports_response import GetInvoicesExportsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetInvoicesExportsResponse from a JSON string
get_invoices_exports_response_instance = GetInvoicesExportsResponse.from_json(json)
# print the JSON string representation of the object
print(GetInvoicesExportsResponse.to_json())

# convert the object into a dict
get_invoices_exports_response_dict = get_invoices_exports_response_instance.to_dict()
# create an instance of GetInvoicesExportsResponse from a dict
get_invoices_exports_response_from_dict = GetInvoicesExportsResponse.from_dict(get_invoices_exports_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


