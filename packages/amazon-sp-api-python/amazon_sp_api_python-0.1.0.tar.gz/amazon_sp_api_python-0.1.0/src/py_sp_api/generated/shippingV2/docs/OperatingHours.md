# OperatingHours

The hours in which the access point shall remain operational

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**closing_time** | [**TimeOfDay**](TimeOfDay.md) |  | [optional] 
**opening_time** | [**TimeOfDay**](TimeOfDay.md) |  | [optional] 
**mid_day_closures** | [**List[TimeOfDay]**](TimeOfDay.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.operating_hours import OperatingHours

# TODO update the JSON string below
json = "{}"
# create an instance of OperatingHours from a JSON string
operating_hours_instance = OperatingHours.from_json(json)
# print the JSON string representation of the object
print(OperatingHours.to_json())

# convert the object into a dict
operating_hours_dict = operating_hours_instance.to_dict()
# create an instance of OperatingHours from a dict
operating_hours_from_dict = OperatingHours.from_dict(operating_hours_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


