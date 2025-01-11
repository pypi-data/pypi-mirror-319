# GetReportDocumentResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ReportDocument**](ReportDocument.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.get_report_document_response import GetReportDocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetReportDocumentResponse from a JSON string
get_report_document_response_instance = GetReportDocumentResponse.from_json(json)
# print the JSON string representation of the object
print(GetReportDocumentResponse.to_json())

# convert the object into a dict
get_report_document_response_dict = get_report_document_response_instance.to_dict()
# create an instance of GetReportDocumentResponse from a dict
get_report_document_response_from_dict = GetReportDocumentResponse.from_dict(get_report_document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


