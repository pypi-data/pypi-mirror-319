# Event

An event of a shipment

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**event_code** | **str** | The event code of a shipment, such as Departed, Received, and ReadyForReceive. | 
**event_time** | **datetime** | The date and time of an event for a shipment. | 
**location** | [**Location**](Location.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.event import Event

# TODO update the JSON string below
json = "{}"
# create an instance of Event from a JSON string
event_instance = Event.from_json(json)
# print the JSON string representation of the object
print(Event.to_json())

# convert the object into a dict
event_dict = event_instance.to_dict()
# create an instance of Event from a dict
event_from_dict = Event.from_dict(event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


