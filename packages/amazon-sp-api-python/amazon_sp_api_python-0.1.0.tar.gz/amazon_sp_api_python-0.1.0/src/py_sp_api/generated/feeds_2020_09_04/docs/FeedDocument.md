# FeedDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feed_document_id** | **str** | The identifier for the feed document. This identifier is unique only in combination with a seller ID. | 
**url** | **str** | A presigned URL for the feed document. If &#x60;compressionAlgorithm&#x60; is not returned, you can download the feed directly from this URL. This URL expires after 5 minutes. | 
**encryption_details** | [**FeedDocumentEncryptionDetails**](FeedDocumentEncryptionDetails.md) |  | 
**compression_algorithm** | **str** | If the feed document contents have been compressed, the compression algorithm used is returned in this property and you must decompress the feed when you download. Otherwise, you can download the feed directly. Refer to [Step 6. Download and decrypt the feed processing report](doc:feeds-api-v2020-09-04-use-case-guide#step-6-download-and-decrypt-the-feed-processing-report) in the use case guide, where sample code is provided. | [optional] 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.feed_document import FeedDocument

# TODO update the JSON string below
json = "{}"
# create an instance of FeedDocument from a JSON string
feed_document_instance = FeedDocument.from_json(json)
# print the JSON string representation of the object
print(FeedDocument.to_json())

# convert the object into a dict
feed_document_dict = feed_document_instance.to_dict()
# create an instance of FeedDocument from a dict
feed_document_from_dict = FeedDocument.from_dict(feed_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


