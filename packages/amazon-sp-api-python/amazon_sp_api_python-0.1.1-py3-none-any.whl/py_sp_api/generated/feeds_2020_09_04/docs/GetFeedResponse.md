# GetFeedResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**Feed**](Feed.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.get_feed_response import GetFeedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeedResponse from a JSON string
get_feed_response_instance = GetFeedResponse.from_json(json)
# print the JSON string representation of the object
print(GetFeedResponse.to_json())

# convert the object into a dict
get_feed_response_dict = get_feed_response_instance.to_dict()
# create an instance of GetFeedResponse from a dict
get_feed_response_from_dict = GetFeedResponse.from_dict(get_feed_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


