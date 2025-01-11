# PostContentDocumentResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 
**content_reference_key** | **str** | A unique reference key for the A+ Content document. A content reference key cannot form a permalink and may change in the future. A content reference key is not guaranteed to match any A+ content identifier. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.post_content_document_response import PostContentDocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostContentDocumentResponse from a JSON string
post_content_document_response_instance = PostContentDocumentResponse.from_json(json)
# print the JSON string representation of the object
print(PostContentDocumentResponse.to_json())

# convert the object into a dict
post_content_document_response_dict = post_content_document_response_instance.to_dict()
# create an instance of PostContentDocumentResponse from a dict
post_content_document_response_from_dict = PostContentDocumentResponse.from_dict(post_content_document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


