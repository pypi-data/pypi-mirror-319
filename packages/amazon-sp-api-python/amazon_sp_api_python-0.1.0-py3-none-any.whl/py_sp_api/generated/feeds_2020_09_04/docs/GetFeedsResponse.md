# GetFeedsResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**List[Feed]**](Feed.md) |  | [optional] 
**next_token** | **str** | Returned when the number of results exceeds pageSize. To get the next page of results, call the getFeeds operation with this token as the only parameter. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.get_feeds_response import GetFeedsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeedsResponse from a JSON string
get_feeds_response_instance = GetFeedsResponse.from_json(json)
# print the JSON string representation of the object
print(GetFeedsResponse.to_json())

# convert the object into a dict
get_feeds_response_dict = get_feeds_response_instance.to_dict()
# create an instance of GetFeedsResponse from a dict
get_feeds_response_from_dict = GetFeedsResponse.from_dict(get_feeds_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


