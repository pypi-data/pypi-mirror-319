# CancelServiceJobByServiceJobIdResponse

Response schema for the `cancelServiceJobByServiceJobId` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.cancel_service_job_by_service_job_id_response import CancelServiceJobByServiceJobIdResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CancelServiceJobByServiceJobIdResponse from a JSON string
cancel_service_job_by_service_job_id_response_instance = CancelServiceJobByServiceJobIdResponse.from_json(json)
# print the JSON string representation of the object
print(CancelServiceJobByServiceJobIdResponse.to_json())

# convert the object into a dict
cancel_service_job_by_service_job_id_response_dict = cancel_service_job_by_service_job_id_response_instance.to_dict()
# create an instance of CancelServiceJobByServiceJobIdResponse from a dict
cancel_service_job_by_service_job_id_response_from_dict = CancelServiceJobByServiceJobIdResponse.from_dict(cancel_service_job_by_service_job_id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


