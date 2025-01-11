# CompleteServiceJobByServiceJobIdResponse

Response schema for the `completeServiceJobByServiceJobId` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.complete_service_job_by_service_job_id_response import CompleteServiceJobByServiceJobIdResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CompleteServiceJobByServiceJobIdResponse from a JSON string
complete_service_job_by_service_job_id_response_instance = CompleteServiceJobByServiceJobIdResponse.from_json(json)
# print the JSON string representation of the object
print(CompleteServiceJobByServiceJobIdResponse.to_json())

# convert the object into a dict
complete_service_job_by_service_job_id_response_dict = complete_service_job_by_service_job_id_response_instance.to_dict()
# create an instance of CompleteServiceJobByServiceJobIdResponse from a dict
complete_service_job_by_service_job_id_response_from_dict = CompleteServiceJobByServiceJobIdResponse.from_dict(complete_service_job_by_service_job_id_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


