# ContentDocument

The A+ Content document. This is the enhanced content that is published to product detail pages.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The A+ Content document name. | 
**content_type** | [**ContentType**](ContentType.md) |  | 
**content_sub_type** | **str** | The A+ Content document subtype. This represents a special-purpose type of an A+ Content document. Not every A+ Content document type will have a subtype, and subtypes may change at any time. | [optional] 
**locale** | **str** | The IETF language tag. This only supports the primary language subtag with one secondary language subtag. The secondary language subtag is almost always a regional designation. This does not support additional subtags beyond the primary and secondary subtags. **Pattern:** ^[a-z]{2,}-[A-Z0-9]{2,}$ | 
**content_module_list** | [**List[ContentModule]**](ContentModule.md) | A list of A+ Content modules. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.content_document import ContentDocument

# TODO update the JSON string below
json = "{}"
# create an instance of ContentDocument from a JSON string
content_document_instance = ContentDocument.from_json(json)
# print the JSON string representation of the object
print(ContentDocument.to_json())

# convert the object into a dict
content_document_dict = content_document_instance.to_dict()
# create an instance of ContentDocument from a dict
content_document_from_dict = ContentDocument.from_dict(content_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


