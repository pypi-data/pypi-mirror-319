# FeedDocumentEncryptionDetails

Encryption details for required client-side encryption and decryption of document contents.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**standard** | **str** | The encryption standard required to encrypt or decrypt the document contents. | 
**initialization_vector** | **str** | The vector to encrypt or decrypt the document contents using Cipher Block Chaining (CBC). | 
**key** | **str** | The encryption key used to encrypt or decrypt the document contents. | 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.feed_document_encryption_details import FeedDocumentEncryptionDetails

# TODO update the JSON string below
json = "{}"
# create an instance of FeedDocumentEncryptionDetails from a JSON string
feed_document_encryption_details_instance = FeedDocumentEncryptionDetails.from_json(json)
# print the JSON string representation of the object
print(FeedDocumentEncryptionDetails.to_json())

# convert the object into a dict
feed_document_encryption_details_dict = feed_document_encryption_details_instance.to_dict()
# create an instance of FeedDocumentEncryptionDetails from a dict
feed_document_encryption_details_from_dict = FeedDocumentEncryptionDetails.from_dict(feed_document_encryption_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


