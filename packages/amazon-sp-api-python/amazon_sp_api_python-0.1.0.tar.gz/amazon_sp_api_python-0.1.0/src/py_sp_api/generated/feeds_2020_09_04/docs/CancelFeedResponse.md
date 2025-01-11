# CancelFeedResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.feeds_2020_09_04.models.cancel_feed_response import CancelFeedResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelFeedResponse from a JSON string
cancel_feed_response_instance = CancelFeedResponse.from_json(json)
# print the JSON string representation of the object
print(CancelFeedResponse.to_json())

# convert the object into a dict
cancel_feed_response_dict = cancel_feed_response_instance.to_dict()
# create an instance of CancelFeedResponse from a dict
cancel_feed_response_from_dict = CancelFeedResponse.from_dict(cancel_feed_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


