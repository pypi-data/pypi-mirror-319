# ExceptionOperatingHours

Defines exceptions to standard operating hours for certain date ranges.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_range** | [**DateRange**](DateRange.md) |  | [optional] 
**operating_hours** | [**OperatingHours**](OperatingHours.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.exception_operating_hours import ExceptionOperatingHours

# TODO update the JSON string below
json = "{}"
# create an instance of ExceptionOperatingHours from a JSON string
exception_operating_hours_instance = ExceptionOperatingHours.from_json(json)
# print the JSON string representation of the object
print(ExceptionOperatingHours.to_json())

# convert the object into a dict
exception_operating_hours_dict = exception_operating_hours_instance.to_dict()
# create an instance of ExceptionOperatingHours from a dict
exception_operating_hours_from_dict = ExceptionOperatingHours.from_dict(exception_operating_hours_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


