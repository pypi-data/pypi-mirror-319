# ReportDocument

Information required for the report document.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**report_document_id** | **str** | The identifier for the report document. This identifier is unique only in combination with a seller ID. | 
**url** | **str** | A presigned URL for the report document. If &#x60;compressionAlgorithm&#x60; is not returned, you can download the report directly from this URL. This URL expires after 5 minutes. | 
**compression_algorithm** | **str** | If the report document contents have been compressed, the compression algorithm used is returned in this property and you must decompress the report when you download. Otherwise, you can download the report directly. Refer to [Step 2. Download the report](https://developer-docs.amazon.com/sp-api/docs/reports-api-v2021-06-30-retrieve-a-report#step-2-download-the-report) in the use case guide, where sample code is provided. | [optional] 

## Example

```python
from py_sp_api.generated.reports_2021_06_30.models.report_document import ReportDocument

# TODO update the JSON string below
json = "{}"
# create an instance of ReportDocument from a JSON string
report_document_instance = ReportDocument.from_json(json)
# print the JSON string representation of the object
print(ReportDocument.to_json())

# convert the object into a dict
report_document_dict = report_document_instance.to_dict()
# create an instance of ReportDocument from a dict
report_document_from_dict = ReportDocument.from_dict(report_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


