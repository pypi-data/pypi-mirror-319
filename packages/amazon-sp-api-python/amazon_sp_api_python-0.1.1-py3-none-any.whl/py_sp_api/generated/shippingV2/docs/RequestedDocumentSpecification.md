# RequestedDocumentSpecification

The document specifications requested. For calls to the purchaseShipment operation, the shipment purchase fails if the specified document specifications are not among those returned in the response to the getRates operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | [**DocumentFormat**](DocumentFormat.md) |  | 
**size** | [**DocumentSize**](DocumentSize.md) |  | 
**dpi** | **int** | The dots per inch (DPI) value used in printing. This value represents a measure of the resolution of the document. | [optional] 
**page_layout** | **str** | Indicates the position of the label on the paper. Should be the same value as returned in getRates response. | [optional] 
**need_file_joining** | **bool** | When true, files should be stitched together. Otherwise, files should be returned separately. Defaults to false. | 
**requested_document_types** | [**List[DocumentType]**](DocumentType.md) | A list of the document types requested. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.requested_document_specification import RequestedDocumentSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of RequestedDocumentSpecification from a JSON string
requested_document_specification_instance = RequestedDocumentSpecification.from_json(json)
# print the JSON string representation of the object
print(RequestedDocumentSpecification.to_json())

# convert the object into a dict
requested_document_specification_dict = requested_document_specification_instance.to_dict()
# create an instance of RequestedDocumentSpecification from a dict
requested_document_specification_from_dict = RequestedDocumentSpecification.from_dict(requested_document_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


