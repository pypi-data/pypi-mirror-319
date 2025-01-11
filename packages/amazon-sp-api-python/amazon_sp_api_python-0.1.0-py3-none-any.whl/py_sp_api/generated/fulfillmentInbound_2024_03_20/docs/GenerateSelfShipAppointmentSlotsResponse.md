# GenerateSelfShipAppointmentSlotsResponse

The `generateSelfShipAppointmentSlots` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_self_ship_appointment_slots_response import GenerateSelfShipAppointmentSlotsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateSelfShipAppointmentSlotsResponse from a JSON string
generate_self_ship_appointment_slots_response_instance = GenerateSelfShipAppointmentSlotsResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateSelfShipAppointmentSlotsResponse.to_json())

# convert the object into a dict
generate_self_ship_appointment_slots_response_dict = generate_self_ship_appointment_slots_response_instance.to_dict()
# create an instance of GenerateSelfShipAppointmentSlotsResponse from a dict
generate_self_ship_appointment_slots_response_from_dict = GenerateSelfShipAppointmentSlotsResponse.from_dict(generate_self_ship_appointment_slots_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


