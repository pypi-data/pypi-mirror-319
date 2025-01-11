# ListContentDocumentAsinRelationsResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**warnings** | [**List[Error]**](Error.md) | A set of messages to the user, such as warnings or comments. | [optional] 
**next_page_token** | **str** | A page token that is returned when the results of the call exceed the page size. To get another page of results, call the operation again, passing in this value with the pageToken parameter. | [optional] 
**asin_metadata_set** | [**List[AsinMetadata]**](AsinMetadata.md) | The set of ASIN metadata. | 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.list_content_document_asin_relations_response import ListContentDocumentAsinRelationsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListContentDocumentAsinRelationsResponse from a JSON string
list_content_document_asin_relations_response_instance = ListContentDocumentAsinRelationsResponse.from_json(json)
# print the JSON string representation of the object
print(ListContentDocumentAsinRelationsResponse.to_json())

# convert the object into a dict
list_content_document_asin_relations_response_dict = list_content_document_asin_relations_response_instance.to_dict()
# create an instance of ListContentDocumentAsinRelationsResponse from a dict
list_content_document_asin_relations_response_from_dict = ListContentDocumentAsinRelationsResponse.from_dict(list_content_document_asin_relations_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


