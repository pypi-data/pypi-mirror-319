# ServiceJob

The job details of a service.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**create_time** | **datetime** | The date and time of the creation of the job in ISO 8601 format. | [optional] 
**service_job_id** | **str** | Amazon identifier for the service job. | [optional] 
**service_job_status** | **str** | The status of the service job. | [optional] 
**scope_of_work** | [**ScopeOfWork**](ScopeOfWork.md) |  | [optional] 
**seller** | [**Seller**](Seller.md) |  | [optional] 
**service_job_provider** | [**ServiceJobProvider**](ServiceJobProvider.md) |  | [optional] 
**preferred_appointment_times** | [**List[AppointmentTime]**](AppointmentTime.md) | A list of appointment windows preferred by the buyer. Included only if the buyer selected appointment windows when creating the order. | [optional] 
**appointments** | [**List[Appointment]**](Appointment.md) | A list of appointments. | [optional] 
**service_order_id** | **str** | The Amazon-defined identifier for an order placed by the buyer, in 3-7-7 format. | [optional] 
**marketplace_id** | **str** | The marketplace identifier. | [optional] 
**store_id** | **str** | The Amazon-defined identifier for the region scope. | [optional] 
**buyer** | [**Buyer**](Buyer.md) |  | [optional] 
**associated_items** | [**List[AssociatedItem]**](AssociatedItem.md) | A list of items associated with the service job. | [optional] 
**service_location** | [**ServiceLocation**](ServiceLocation.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.services.models.service_job import ServiceJob

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceJob from a JSON string
service_job_instance = ServiceJob.from_json(json)
# print the JSON string representation of the object
print(ServiceJob.to_json())

# convert the object into a dict
service_job_dict = service_job_instance.to_dict()
# create an instance of ServiceJob from a dict
service_job_from_dict = ServiceJob.from_dict(service_job_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


