# Poa

Proof of Appointment (POA) details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**appointment_time** | [**AppointmentTime**](AppointmentTime.md) |  | [optional] 
**technicians** | [**List[Technician]**](Technician.md) | A list of technicians. | [optional] 
**uploading_technician** | **str** | The identifier of the technician who uploaded the POA. | [optional] 
**upload_time** | **datetime** | The date and time when the POA was uploaded in ISO 8601 format. | [optional] 
**poa_type** | **str** | The type of POA uploaded. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.poa import Poa

# TODO update the JSON string below
json = "{}"
# create an instance of Poa from a JSON string
poa_instance = Poa.from_json(json)
# print the JSON string representation of the object
print(Poa.to_json())

# convert the object into a dict
poa_dict = poa_instance.to_dict()
# create an instance of Poa from a dict
poa_from_dict = Poa.from_dict(poa_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


