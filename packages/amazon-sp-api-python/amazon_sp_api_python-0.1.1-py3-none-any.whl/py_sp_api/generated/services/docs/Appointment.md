# Appointment

The details of an appointment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**appointment_id** | **str** | The appointment identifier. | [optional] 
**appointment_status** | **str** | The status of the appointment. | [optional] 
**appointment_time** | [**AppointmentTime**](AppointmentTime.md) |  | [optional] 
**assigned_technicians** | [**List[Technician]**](Technician.md) | A list of technicians assigned to the service job. | [optional] 
**rescheduled_appointment_id** | **str** | The appointment identifier. | [optional] 
**poa** | [**Poa**](Poa.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.services.models.appointment import Appointment

# TODO update the JSON string below
json = "{}"
# create an instance of Appointment from a JSON string
appointment_instance = Appointment.from_json(json)
# print the JSON string representation of the object
print(Appointment.to_json())

# convert the object into a dict
appointment_dict = appointment_instance.to_dict()
# create an instance of Appointment from a dict
appointment_from_dict = Appointment.from_dict(appointment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


