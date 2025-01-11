# CreateFeedDocumentResponse

Information required to upload a feed document's contents.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feed_document_id** | **str** | The identifier of the feed document. | 
**url** | **str** | The presigned URL for uploading the feed contents. This URL expires after 5 minutes. | 

## Example

```python
from py_sp_api.generated.feeds_2021_06_30.models.create_feed_document_response import CreateFeedDocumentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFeedDocumentResponse from a JSON string
create_feed_document_response_instance = CreateFeedDocumentResponse.from_json(json)
# print the JSON string representation of the object
print(CreateFeedDocumentResponse.to_json())

# convert the object into a dict
create_feed_document_response_dict = create_feed_document_response_instance.to_dict()
# create an instance of CreateFeedDocumentResponse from a dict
create_feed_document_response_from_dict = CreateFeedDocumentResponse.from_dict(create_feed_document_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


