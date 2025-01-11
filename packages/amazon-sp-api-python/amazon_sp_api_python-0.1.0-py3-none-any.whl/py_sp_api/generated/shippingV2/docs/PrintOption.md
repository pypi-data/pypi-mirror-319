# PrintOption

The format options available for a label.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**supported_dpis** | **List[int]** | A list of the supported DPI options for a document. | [optional] 
**supported_page_layouts** | **List[str]** | A list of the supported page layout options for a document. | 
**supported_file_joining_options** | **List[bool]** | A list of the supported needFileJoining boolean values for a document. | 
**supported_document_details** | [**List[SupportedDocumentDetail]**](SupportedDocumentDetail.md) | A list of the supported documented details. | 

## Example

```python
from py_sp_api.generated.shippingV2.models.print_option import PrintOption

# TODO update the JSON string below
json = "{}"
# create an instance of PrintOption from a JSON string
print_option_instance = PrintOption.from_json(json)
# print the JSON string representation of the object
print(PrintOption.to_json())

# convert the object into a dict
print_option_dict = print_option_instance.to_dict()
# create an instance of PrintOption from a dict
print_option_from_dict = PrintOption.from_dict(print_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


