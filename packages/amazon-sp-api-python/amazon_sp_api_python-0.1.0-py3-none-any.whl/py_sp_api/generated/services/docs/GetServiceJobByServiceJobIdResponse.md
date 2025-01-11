# GetServiceJobByServiceJobIdResponse

The response schema for the `getServiceJobByServiceJobId` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ServiceJob**](ServiceJob.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.get_service_job_by_service_job_id_response import GetServiceJobByServiceJobIdResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetServiceJobByServiceJobIdResponse from a JSON string
get_service_job_by_service_job_id_response_instance = GetServiceJobByServiceJobIdResponse.from_json(json)
# print the JSON string representation of the object
print(GetServiceJobByServiceJobIdResponse.to_json())

# convert the object into a dict
get_service_job_by_service_job_id_response_dict = get_service_job_by_service_job_id_response_instance.to_dict()
# create an instance of GetServiceJobByServiceJobIdResponse from a dict
get_service_job_by_service_job_id_response_from_dict = GetServiceJobByServiceJobIdResponse.from_dict(get_service_job_by_service_job_id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


