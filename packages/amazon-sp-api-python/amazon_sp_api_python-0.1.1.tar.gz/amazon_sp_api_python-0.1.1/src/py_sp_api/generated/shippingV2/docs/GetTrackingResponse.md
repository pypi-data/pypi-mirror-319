# GetTrackingResponse

The response schema for the getTracking operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetTrackingResult**](GetTrackingResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_tracking_response import GetTrackingResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetTrackingResponse from a JSON string
get_tracking_response_instance = GetTrackingResponse.from_json(json)
# print the JSON string representation of the object
print(GetTrackingResponse.to_json())

# convert the object into a dict
get_tracking_response_dict = get_tracking_response_instance.to_dict()
# create an instance of GetTrackingResponse from a dict
get_tracking_response_from_dict = GetTrackingResponse.from_dict(get_tracking_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


