# PostContentDocumentAsinRelationsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.post_content_document_asin_relations_response import PostContentDocumentAsinRelationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PostContentDocumentAsinRelationsResponse from a JSON string
post_content_document_asin_relations_response_instance = PostContentDocumentAsinRelationsResponse.from_json(json)
# print the JSON string representation of the object
print(PostContentDocumentAsinRelationsResponse.to_json())

# convert the object into a dict
post_content_document_asin_relations_response_dict = post_content_document_asin_relations_response_instance.to_dict()
# create an instance of PostContentDocumentAsinRelationsResponse from a dict
post_content_document_asin_relations_response_from_dict = PostContentDocumentAsinRelationsResponse.from_dict(post_content_document_asin_relations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


