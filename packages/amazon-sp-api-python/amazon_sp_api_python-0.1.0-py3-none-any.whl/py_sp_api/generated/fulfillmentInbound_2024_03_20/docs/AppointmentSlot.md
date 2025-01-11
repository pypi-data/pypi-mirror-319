# AppointmentSlot

The fulfillment center appointment slot for the transportation option.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**slot_id** | **str** | An identifier to a self-ship appointment slot. | 
**slot_time** | [**AppointmentSlotTime**](AppointmentSlotTime.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.appointment_slot import AppointmentSlot

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentSlot from a JSON string
appointment_slot_instance = AppointmentSlot.from_json(json)
# print the JSON string representation of the object
print(AppointmentSlot.to_json())

# convert the object into a dict
appointment_slot_dict = appointment_slot_instance.to_dict()
# create an instance of AppointmentSlot from a dict
appointment_slot_from_dict = AppointmentSlot.from_dict(appointment_slot_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


