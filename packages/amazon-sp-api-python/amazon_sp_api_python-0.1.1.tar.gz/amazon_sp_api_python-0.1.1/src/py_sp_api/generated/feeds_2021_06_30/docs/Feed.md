# Feed

Detailed information about the feed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**feed_id** | **str** | The identifier for the feed. This identifier is unique only in combination with a seller ID. | 
**feed_type** | **str** | The feed type. | 
**marketplace_ids** | **List[str]** | A list of identifiers for the marketplaces that the feed is applied to. | [optional] 
**created_time** | **datetime** | The date and time when the feed was created, in ISO 8601 date time format. | 
**processing_status** | **str** | The processing status of the feed. | 
**processing_start_time** | **datetime** | The date and time when feed processing started, in ISO 8601 date time format. | [optional] 
**processing_end_time** | **datetime** | The date and time when feed processing completed, in ISO 8601 date time format. | [optional] 
**result_feed_document_id** | **str** | The identifier for the feed document. This identifier is unique only in combination with a seller ID. | [optional] 

## Example

```python
from py_sp_api.generated.feeds_2021_06_30.models.feed import Feed

# TODO update the JSON string below
json = "{}"
# create an instance of Feed from a JSON string
feed_instance = Feed.from_json(json)
# print the JSON string representation of the object
print(Feed.to_json())

# convert the object into a dict
feed_dict = feed_instance.to_dict()
# create an instance of Feed from a dict
feed_from_dict = Feed.from_dict(feed_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


