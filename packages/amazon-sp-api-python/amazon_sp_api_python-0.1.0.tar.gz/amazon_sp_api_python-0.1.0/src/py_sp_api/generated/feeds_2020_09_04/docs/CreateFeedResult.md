# CreateFeedResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feed_id** | **str** | The identifier for the feed. This identifier is unique only in combination with a seller ID. | 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.create_feed_result import CreateFeedResult

# TODO update the JSON string below
json = "{}"
# create an instance of CreateFeedResult from a JSON string
create_feed_result_instance = CreateFeedResult.from_json(json)
# print the JSON string representation of the object
print(CreateFeedResult.to_json())

# convert the object into a dict
create_feed_result_dict = create_feed_result_instance.to_dict()
# create an instance of CreateFeedResult from a dict
create_feed_result_from_dict = CreateFeedResult.from_dict(create_feed_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


