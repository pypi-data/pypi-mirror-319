# GetInvoicesDocumentResponse

Success.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**invoices_document** | [**InvoicesDocument**](InvoicesDocument.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.InvoicesApiModel_2024_06_19.models.get_invoices_document_response import GetInvoicesDocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetInvoicesDocumentResponse from a JSON string
get_invoices_document_response_instance = GetInvoicesDocumentResponse.from_json(json)
# print the JSON string representation of the object
print(GetInvoicesDocumentResponse.to_json())

# convert the object into a dict
get_invoices_document_response_dict = get_invoices_document_response_instance.to_dict()
# create an instance of GetInvoicesDocumentResponse from a dict
get_invoices_document_response_from_dict = GetInvoicesDocumentResponse.from_dict(get_invoices_document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


