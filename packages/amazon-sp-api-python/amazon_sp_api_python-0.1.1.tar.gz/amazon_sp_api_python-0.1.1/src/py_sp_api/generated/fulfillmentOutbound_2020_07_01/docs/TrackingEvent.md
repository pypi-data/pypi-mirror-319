# TrackingEvent

Information for tracking package deliveries.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_date** | **datetime** | Date timestamp | 
**event_address** | [**TrackingAddress**](TrackingAddress.md) |  | 
**event_code** | [**EventCode**](EventCode.md) |  | 
**event_description** | **str** | A description for the corresponding event code. | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.tracking_event import TrackingEvent

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingEvent from a JSON string
tracking_event_instance = TrackingEvent.from_json(json)
# print the JSON string representation of the object
print(TrackingEvent.to_json())

# convert the object into a dict
tracking_event_dict = tracking_event_instance.to_dict()
# create an instance of TrackingEvent from a dict
tracking_event_from_dict = TrackingEvent.from_dict(tracking_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


