# TimeOfDay

Denotes time of the day, used for defining opening or closing time of access points

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hour_of_day** | **int** |  | [optional] 
**minute_of_hour** | **int** |  | [optional] 
**second_of_minute** | **int** |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.time_of_day import TimeOfDay

# TODO update the JSON string below
json = "{}"
# create an instance of TimeOfDay from a JSON string
time_of_day_instance = TimeOfDay.from_json(json)
# print the JSON string representation of the object
print(TimeOfDay.to_json())

# convert the object into a dict
time_of_day_dict = time_of_day_instance.to_dict()
# create an instance of TimeOfDay from a dict
time_of_day_from_dict = TimeOfDay.from_dict(time_of_day_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


