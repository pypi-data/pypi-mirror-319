# CarrierAppointment

Contains details for a transportation carrier appointment. This appointment is vended out by Amazon and is an indicator for when a transportation carrier is accepting shipments to be picked up.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**end_time** | **datetime** | The end timestamp of the appointment in UTC. | 
**start_time** | **datetime** | The start timestamp of the appointment in UTC. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.carrier_appointment import CarrierAppointment

# TODO update the JSON string below
json = "{}"
# create an instance of CarrierAppointment from a JSON string
carrier_appointment_instance = CarrierAppointment.from_json(json)
# print the JSON string representation of the object
print(CarrierAppointment.to_json())

# convert the object into a dict
carrier_appointment_dict = carrier_appointment_instance.to_dict()
# create an instance of CarrierAppointment from a dict
carrier_appointment_from_dict = CarrierAppointment.from_dict(carrier_appointment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


