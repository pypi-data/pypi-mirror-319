# InvoicesDocument

An object that contains the `documentId` and an S3 pre-signed URL that you can use to download the specified file.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoices_document_id** | **str** | The identifier of the export document. | [optional] 
**invoices_document_url** | **str** | A pre-signed URL that you can use to download the invoices document in zip format. This URL expires after 30 seconds. | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.invoices_document import InvoicesDocument

# TODO update the JSON string below
json = "{}"
# create an instance of InvoicesDocument from a JSON string
invoices_document_instance = InvoicesDocument.from_json(json)
# print the JSON string representation of the object
print(InvoicesDocument.to_json())

# convert the object into a dict
invoices_document_dict = invoices_document_instance.to_dict()
# create an instance of InvoicesDocument from a dict
invoices_document_from_dict = InvoicesDocument.from_dict(invoices_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


