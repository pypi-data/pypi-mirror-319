# SupportedDocumentSpecification

Document specification that is supported for a service offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | [**DocumentFormat**](DocumentFormat.md) |  | 
**size** | [**DocumentSize**](DocumentSize.md) |  | 
**print_options** | [**List[PrintOption]**](PrintOption.md) | A list of the format options for a label. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.supported_document_specification import SupportedDocumentSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of SupportedDocumentSpecification from a JSON string
supported_document_specification_instance = SupportedDocumentSpecification.from_json(json)
# print the JSON string representation of the object
print(SupportedDocumentSpecification.to_json())

# convert the object into a dict
supported_document_specification_dict = supported_document_specification_instance.to_dict()
# create an instance of SupportedDocumentSpecification from a dict
supported_document_specification_from_dict = SupportedDocumentSpecification.from_dict(supported_document_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


