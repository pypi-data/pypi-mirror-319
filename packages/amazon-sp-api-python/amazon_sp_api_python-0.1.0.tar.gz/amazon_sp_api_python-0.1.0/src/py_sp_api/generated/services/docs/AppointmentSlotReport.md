# AppointmentSlotReport

Availability information as per the service context queried.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scheduling_type** | **str** | Defines the type of slots. | [optional] 
**start_time** | **datetime** | Start Time from which the appointment slots are generated in ISO 8601 format. | [optional] 
**end_time** | **datetime** | End Time up to which the appointment slots are generated in ISO 8601 format. | [optional] 
**appointment_slots** | [**List[AppointmentSlot]**](AppointmentSlot.md) | A list of time windows along with associated capacity in which the service can be performed. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.appointment_slot_report import AppointmentSlotReport

# TODO update the JSON string below
json = "{}"
# create an instance of AppointmentSlotReport from a JSON string
appointment_slot_report_instance = AppointmentSlotReport.from_json(json)
# print the JSON string representation of the object
print(AppointmentSlotReport.to_json())

# convert the object into a dict
appointment_slot_report_dict = appointment_slot_report_instance.to_dict()
# create an instance of AppointmentSlotReport from a dict
appointment_slot_report_from_dict = AppointmentSlotReport.from_dict(appointment_slot_report_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


