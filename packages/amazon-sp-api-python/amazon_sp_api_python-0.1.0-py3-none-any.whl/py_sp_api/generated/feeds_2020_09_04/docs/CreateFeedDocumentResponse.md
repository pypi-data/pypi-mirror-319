# CreateFeedDocumentResponse

The response for the createFeedDocument operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CreateFeedDocumentResult**](CreateFeedDocumentResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_document_response import CreateFeedDocumentResponse

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


