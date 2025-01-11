# CollectionsFormDocument

Collection Form Document Details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**base64_encoded_content** | **str** | Base64 document Value of Collection. | [optional] 
**document_format** | **str** | Collection Document format is PDF. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.collections_form_document import CollectionsFormDocument

# TODO update the JSON string below
json = "{}"
# create an instance of CollectionsFormDocument from a JSON string
collections_form_document_instance = CollectionsFormDocument.from_json(json)
# print the JSON string representation of the object
print(CollectionsFormDocument.to_json())

# convert the object into a dict
collections_form_document_dict = collections_form_document_instance.to_dict()
# create an instance of CollectionsFormDocument from a dict
collections_form_document_from_dict = CollectionsFormDocument.from_dict(collections_form_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


