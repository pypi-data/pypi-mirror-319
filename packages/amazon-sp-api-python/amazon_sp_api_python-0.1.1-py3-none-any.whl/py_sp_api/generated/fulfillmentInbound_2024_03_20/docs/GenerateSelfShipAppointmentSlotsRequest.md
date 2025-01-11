# GenerateSelfShipAppointmentSlotsRequest

The `generateSelfShipAppointmentSlots` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**desired_end_date** | **datetime** | The desired end date. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format. | [optional] 
**desired_start_date** | **datetime** | The desired start date. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_self_ship_appointment_slots_request import GenerateSelfShipAppointmentSlotsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateSelfShipAppointmentSlotsRequest from a JSON string
generate_self_ship_appointment_slots_request_instance = GenerateSelfShipAppointmentSlotsRequest.from_json(json)
# print the JSON string representation of the object
print(GenerateSelfShipAppointmentSlotsRequest.to_json())

# convert the object into a dict
generate_self_ship_appointment_slots_request_dict = generate_self_ship_appointment_slots_request_instance.to_dict()
# create an instance of GenerateSelfShipAppointmentSlotsRequest from a dict
generate_self_ship_appointment_slots_request_from_dict = GenerateSelfShipAppointmentSlotsRequest.from_dict(generate_self_ship_appointment_slots_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


