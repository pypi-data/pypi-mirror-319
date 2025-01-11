# OperatingHour

The operating hour schema

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | **str** | The opening time, ISO 8601 formatted timestamp without date, HH:mm. | [optional] 
**end_time** | **str** | The closing time, ISO 8601 formatted timestamp without date, HH:mm. | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.operating_hour import OperatingHour

# TODO update the JSON string below
json = "{}"
# create an instance of OperatingHour from a JSON string
operating_hour_instance = OperatingHour.from_json(json)
# print the JSON string representation of the object
print(OperatingHour.to_json())

# convert the object into a dict
operating_hour_dict = operating_hour_instance.to_dict()
# create an instance of OperatingHour from a dict
operating_hour_from_dict = OperatingHour.from_dict(operating_hour_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


