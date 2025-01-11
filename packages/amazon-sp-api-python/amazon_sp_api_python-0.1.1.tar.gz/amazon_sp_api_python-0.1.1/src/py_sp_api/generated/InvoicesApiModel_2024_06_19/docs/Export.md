# Export

Detailed information about the export.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_message** | **str** | When the export generation fails, this attribute contains a description of the error. | [optional] 
**export_id** | **str** | The export identifier. | [optional] 
**generate_export_finished_at** | **datetime** | The date and time when the export generation finished. Vales are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**generate_export_started_at** | **datetime** | The date and time when the export generation started. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format. | [optional] 
**invoices_document_ids** | **List[str]** | The identifier for the export documents. To get the information required to retrieve the export document&#39;s contents, pass each ID in the &#x60;getInvoicesDocument&#x60; operation.  This list is empty until the status is &#x60;DONE&#x60;. | [optional] 
**status** | [**ExportStatus**](ExportStatus.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.export import Export

# TODO update the JSON string below
json = "{}"
# create an instance of Export from a JSON string
export_instance = Export.from_json(json)
# print the JSON string representation of the object
print(Export.to_json())

# convert the object into a dict
export_dict = export_instance.to_dict()
# create an instance of Export from a dict
export_from_dict = Export.from_dict(export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


