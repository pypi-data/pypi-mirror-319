# GetSelfShipAppointmentSlotsResponse

The `getSelfShipAppointmentSlots` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**self_ship_appointment_slots_availability** | [**SelfShipAppointmentSlotsAvailability**](SelfShipAppointmentSlotsAvailability.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.get_self_ship_appointment_slots_response import GetSelfShipAppointmentSlotsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetSelfShipAppointmentSlotsResponse from a JSON string
get_self_ship_appointment_slots_response_instance = GetSelfShipAppointmentSlotsResponse.from_json(json)
# print the JSON string representation of the object
print(GetSelfShipAppointmentSlotsResponse.to_json())

# convert the object into a dict
get_self_ship_appointment_slots_response_dict = get_self_ship_appointment_slots_response_instance.to_dict()
# create an instance of GetSelfShipAppointmentSlotsResponse from a dict
get_self_ship_appointment_slots_response_from_dict = GetSelfShipAppointmentSlotsResponse.from_dict(get_self_ship_appointment_slots_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


