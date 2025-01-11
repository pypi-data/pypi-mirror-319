# CreateFeedResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feed_id** | **str** | The identifier for the feed. This identifier is unique only in combination with a seller ID. | 

## Example

```python
from py_sp_api.generated.feeds_2021_06_30.models.create_feed_response import CreateFeedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFeedResponse from a JSON string
create_feed_response_instance = CreateFeedResponse.from_json(json)
# print the JSON string representation of the object
print(CreateFeedResponse.to_json())

# convert the object into a dict
create_feed_response_dict = create_feed_response_instance.to_dict()
# create an instance of CreateFeedResponse from a dict
create_feed_response_from_dict = CreateFeedResponse.from_dict(create_feed_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


