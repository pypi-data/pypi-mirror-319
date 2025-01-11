# SupportedDocumentDetail

The supported document types for a service offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | [**DocumentType**](DocumentType.md) |  | 
**is_mandatory** | **bool** | When true, the supported document type is required. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.supported_document_detail import SupportedDocumentDetail

# TODO update the JSON string below
json = "{}"
# create an instance of SupportedDocumentDetail from a JSON string
supported_document_detail_instance = SupportedDocumentDetail.from_json(json)
# print the JSON string representation of the object
print(SupportedDocumentDetail.to_json())

# convert the object into a dict
supported_document_detail_dict = supported_document_detail_instance.to_dict()
# create an instance of SupportedDocumentDetail from a dict
supported_document_detail_from_dict = SupportedDocumentDetail.from_dict(supported_document_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


