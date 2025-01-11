# CreateFeedDocumentSpecification


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_type** | **str** | The content type of the feed. | 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_document_specification import CreateFeedDocumentSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFeedDocumentSpecification from a JSON string
create_feed_document_specification_instance = CreateFeedDocumentSpecification.from_json(json)
# print the JSON string representation of the object
print(CreateFeedDocumentSpecification.to_json())

# convert the object into a dict
create_feed_document_specification_dict = create_feed_document_specification_instance.to_dict()
# create an instance of CreateFeedDocumentSpecification from a dict
create_feed_document_specification_from_dict = CreateFeedDocumentSpecification.from_dict(create_feed_document_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


