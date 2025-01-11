# ReportDocumentEncryptionDetails

Encryption details required for decryption of a report document's contents.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**standard** | **str** | The encryption standard required to decrypt the document contents. | 
**initialization_vector** | **str** | The vector to decrypt the document contents using Cipher Block Chaining (CBC). | 
**key** | **str** | The encryption key used to decrypt the document contents. | 

## Example

```python
from py_sp_api.generated.reports_2020_09_04.models.report_document_encryption_details import ReportDocumentEncryptionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ReportDocumentEncryptionDetails from a JSON string
report_document_encryption_details_instance = ReportDocumentEncryptionDetails.from_json(json)
# print the JSON string representation of the object
print(ReportDocumentEncryptionDetails.to_json())

# convert the object into a dict
report_document_encryption_details_dict = report_document_encryption_details_instance.to_dict()
# create an instance of ReportDocumentEncryptionDetails from a dict
report_document_encryption_details_from_dict = ReportDocumentEncryptionDetails.from_dict(report_document_encryption_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


