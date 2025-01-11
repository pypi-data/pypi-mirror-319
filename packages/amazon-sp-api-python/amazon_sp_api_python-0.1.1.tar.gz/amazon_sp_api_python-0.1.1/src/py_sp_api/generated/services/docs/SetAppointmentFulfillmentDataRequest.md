# SetAppointmentFulfillmentDataRequest

Input for set appointment fulfillment data operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_time** | [**FulfillmentTime**](FulfillmentTime.md) |  | [optional] 
**appointment_resources** | [**List[AppointmentResource]**](AppointmentResource.md) | List of resources that performs or performed job appointment fulfillment. | [optional] 
**fulfillment_documents** | [**List[FulfillmentDocument]**](FulfillmentDocument.md) | List of documents captured during service appointment fulfillment. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.set_appointment_fulfillment_data_request import SetAppointmentFulfillmentDataRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetAppointmentFulfillmentDataRequest from a JSON string
set_appointment_fulfillment_data_request_instance = SetAppointmentFulfillmentDataRequest.from_json(json)
# print the JSON string representation of the object
print(SetAppointmentFulfillmentDataRequest.to_json())

# convert the object into a dict
set_appointment_fulfillment_data_request_dict = set_appointment_fulfillment_data_request_instance.to_dict()
# create an instance of SetAppointmentFulfillmentDataRequest from a dict
set_appointment_fulfillment_data_request_from_dict = SetAppointmentFulfillmentDataRequest.from_dict(set_appointment_fulfillment_data_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


