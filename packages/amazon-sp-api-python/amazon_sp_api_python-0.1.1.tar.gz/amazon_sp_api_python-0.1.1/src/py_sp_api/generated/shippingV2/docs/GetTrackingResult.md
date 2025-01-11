# GetTrackingResult

The payload for the getTracking operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_id** | **str** | The carrier generated identifier for a package in a purchased shipment. | 
**alternate_leg_tracking_id** | **str** | The carrier generated reverse identifier for a returned package in a purchased shipment. | 
**event_history** | [**List[Event]**](Event.md) | A list of tracking events. | 
**promised_delivery_date** | **datetime** | The date and time by which the shipment is promised to be delivered. | 
**summary** | [**TrackingSummary**](TrackingSummary.md) |  | 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_tracking_result import GetTrackingResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetTrackingResult from a JSON string
get_tracking_result_instance = GetTrackingResult.from_json(json)
# print the JSON string representation of the object
print(GetTrackingResult.to_json())

# convert the object into a dict
get_tracking_result_dict = get_tracking_result_instance.to_dict()
# create an instance of GetTrackingResult from a dict
get_tracking_result_from_dict = GetTrackingResult.from_dict(get_tracking_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


