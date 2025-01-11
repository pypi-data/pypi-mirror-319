# PostContentDocumentAsinRelationsRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin_set** | **List[str]** | The set of ASINs. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.post_content_document_asin_relations_request import PostContentDocumentAsinRelationsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PostContentDocumentAsinRelationsRequest from a JSON string
post_content_document_asin_relations_request_instance = PostContentDocumentAsinRelationsRequest.from_json(json)
# print the JSON string representation of the object
print(PostContentDocumentAsinRelationsRequest.to_json())

# convert the object into a dict
post_content_document_asin_relations_request_dict = post_content_document_asin_relations_request_instance.to_dict()
# create an instance of PostContentDocumentAsinRelationsRequest from a dict
post_content_document_asin_relations_request_from_dict = PostContentDocumentAsinRelationsRequest.from_dict(post_content_document_asin_relations_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


