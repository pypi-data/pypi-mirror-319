# CreateFeedDocumentResult

Information required to encrypt and upload a feed document's contents.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feed_document_id** | **str** | The identifier of the feed document. | 
**url** | **str** | The presigned URL for uploading the feed contents. This URL expires after 5 minutes. | 
**encryption_details** | [**FeedDocumentEncryptionDetails**](FeedDocumentEncryptionDetails.md) |  | 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_document_result import CreateFeedDocumentResult

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFeedDocumentResult from a JSON string
create_feed_document_result_instance = CreateFeedDocumentResult.from_json(json)
# print the JSON string representation of the object
print(CreateFeedDocumentResult.to_json())

# convert the object into a dict
create_feed_document_result_dict = create_feed_document_result_instance.to_dict()
# create an instance of CreateFeedDocumentResult from a dict
create_feed_document_result_from_dict = CreateFeedDocumentResult.from_dict(create_feed_document_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


