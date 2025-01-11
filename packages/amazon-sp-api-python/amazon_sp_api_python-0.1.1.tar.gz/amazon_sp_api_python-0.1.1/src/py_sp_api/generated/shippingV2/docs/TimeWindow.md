# TimeWindow

The start and end time that specifies the time interval of an event.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **datetime** | The start time of the time window. | [optional] 
**end** | **datetime** | The end time of the time window. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.time_window import TimeWindow

# TODO update the JSON string below
json = "{}"
# create an instance of TimeWindow from a JSON string
time_window_instance = TimeWindow.from_json(json)
# print the JSON string representation of the object
print(TimeWindow.to_json())

# convert the object into a dict
time_window_dict = time_window_instance.to_dict()
# create an instance of TimeWindow from a dict
time_window_from_dict = TimeWindow.from_dict(time_window_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


