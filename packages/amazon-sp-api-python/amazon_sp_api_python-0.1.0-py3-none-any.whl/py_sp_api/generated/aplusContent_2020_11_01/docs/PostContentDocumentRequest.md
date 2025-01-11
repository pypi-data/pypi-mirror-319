# PostContentDocumentRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_document** | [**ContentDocument**](ContentDocument.md) |  | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.post_content_document_request import PostContentDocumentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PostContentDocumentRequest from a JSON string
post_content_document_request_instance = PostContentDocumentRequest.from_json(json)
# print the JSON string representation of the object
print(PostContentDocumentRequest.to_json())

# convert the object into a dict
post_content_document_request_dict = post_content_document_request_instance.to_dict()
# create an instance of PostContentDocumentRequest from a dict
post_content_document_request_from_dict = PostContentDocumentRequest.from_dict(post_content_document_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


