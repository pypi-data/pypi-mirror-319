# GetServiceJobsResponse

Response schema for the `getServiceJobs` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**JobListing**](JobListing.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.get_service_jobs_response import GetServiceJobsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetServiceJobsResponse from a JSON string
get_service_jobs_response_instance = GetServiceJobsResponse.from_json(json)
# print the JSON string representation of the object
print(GetServiceJobsResponse.to_json())

# convert the object into a dict
get_service_jobs_response_dict = get_service_jobs_response_instance.to_dict()
# create an instance of GetServiceJobsResponse from a dict
get_service_jobs_response_from_dict = GetServiceJobsResponse.from_dict(get_service_jobs_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


