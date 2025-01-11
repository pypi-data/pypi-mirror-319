# TimeSlot

A time window to hand over an Easy Ship package to Amazon Logistics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**slot_id** | **str** | A string of up to 255 characters. | 
**start_time** | **datetime** | A datetime value in ISO 8601 format. | [optional] 
**end_time** | **datetime** | A datetime value in ISO 8601 format. | [optional] 
**handover_method** | [**HandoverMethod**](HandoverMethod.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.time_slot import TimeSlot

# TODO update the JSON string below
json = "{}"
# create an instance of TimeSlot from a JSON string
time_slot_instance = TimeSlot.from_json(json)
# print the JSON string representation of the object
print(TimeSlot.to_json())

# convert the object into a dict
time_slot_dict = time_slot_instance.to_dict()
# create an instance of TimeSlot from a dict
time_slot_from_dict = TimeSlot.from_dict(time_slot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


