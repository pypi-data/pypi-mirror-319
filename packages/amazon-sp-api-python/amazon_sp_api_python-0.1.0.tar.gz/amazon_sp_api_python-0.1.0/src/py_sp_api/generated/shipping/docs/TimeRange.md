# TimeRange

The time range.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start** | **datetime** | The start date and time. This defaults to the current date and time. | [optional] 
**end** | **datetime** | The end date and time. This must come after the value of start. This defaults to the next business day from the start. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.time_range import TimeRange

# TODO update the JSON string below
json = "{}"
# create an instance of TimeRange from a JSON string
time_range_instance = TimeRange.from_json(json)
# print the JSON string representation of the object
print(TimeRange.to_json())

# convert the object into a dict
time_range_dict = time_range_instance.to_dict()
# create an instance of TimeRange from a dict
time_range_from_dict = TimeRange.from_dict(time_range_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


