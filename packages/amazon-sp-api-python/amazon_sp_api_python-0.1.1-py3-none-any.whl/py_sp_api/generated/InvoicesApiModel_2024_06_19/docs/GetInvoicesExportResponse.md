# GetInvoicesExportResponse

Success.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**export** | [**Export**](Export.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.get_invoices_export_response import GetInvoicesExportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetInvoicesExportResponse from a JSON string
get_invoices_export_response_instance = GetInvoicesExportResponse.from_json(json)
# print the JSON string representation of the object
print(GetInvoicesExportResponse.to_json())

# convert the object into a dict
get_invoices_export_response_dict = get_invoices_export_response_instance.to_dict()
# create an instance of GetInvoicesExportResponse from a dict
get_invoices_export_response_from_dict = GetInvoicesExportResponse.from_dict(get_invoices_export_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


