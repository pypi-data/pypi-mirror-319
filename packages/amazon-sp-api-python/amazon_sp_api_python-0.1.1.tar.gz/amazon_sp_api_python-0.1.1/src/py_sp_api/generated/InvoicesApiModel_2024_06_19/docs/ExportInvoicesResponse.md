# ExportInvoicesResponse

Success.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**export_id** | **str** | The export identifier. | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.export_invoices_response import ExportInvoicesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ExportInvoicesResponse from a JSON string
export_invoices_response_instance = ExportInvoicesResponse.from_json(json)
# print the JSON string representation of the object
print(ExportInvoicesResponse.to_json())

# convert the object into a dict
export_invoices_response_dict = export_invoices_response_instance.to_dict()
# create an instance of ExportInvoicesResponse from a dict
export_invoices_response_from_dict = ExportInvoicesResponse.from_dict(export_invoices_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


