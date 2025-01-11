# OperatingHoursByDay

The operating hours per day

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**monday** | [**List[OperatingHour]**](OperatingHour.md) | A list of Operating Hours. | [optional] 
**tuesday** | [**List[OperatingHour]**](OperatingHour.md) | A list of Operating Hours. | [optional] 
**wednesday** | [**List[OperatingHour]**](OperatingHour.md) | A list of Operating Hours. | [optional] 
**thursday** | [**List[OperatingHour]**](OperatingHour.md) | A list of Operating Hours. | [optional] 
**friday** | [**List[OperatingHour]**](OperatingHour.md) | A list of Operating Hours. | [optional] 
**saturday** | [**List[OperatingHour]**](OperatingHour.md) | A list of Operating Hours. | [optional] 
**sunday** | [**List[OperatingHour]**](OperatingHour.md) | A list of Operating Hours. | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.operating_hours_by_day import OperatingHoursByDay

# TODO update the JSON string below
json = "{}"
# create an instance of OperatingHoursByDay from a JSON string
operating_hours_by_day_instance = OperatingHoursByDay.from_json(json)
# print the JSON string representation of the object
print(OperatingHoursByDay.to_json())

# convert the object into a dict
operating_hours_by_day_dict = operating_hours_by_day_instance.to_dict()
# create an instance of OperatingHoursByDay from a dict
operating_hours_by_day_from_dict = OperatingHoursByDay.from_dict(operating_hours_by_day_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


