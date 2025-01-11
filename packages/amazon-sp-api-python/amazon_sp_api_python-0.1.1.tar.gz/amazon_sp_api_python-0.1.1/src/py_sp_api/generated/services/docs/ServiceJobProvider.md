# ServiceJobProvider

Information about the service job provider.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**service_job_provider_id** | **str** | The identifier of the service job provider. | [optional] 

## Example

```python
from py_sp_api.generated.services.models.service_job_provider import ServiceJobProvider

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceJobProvider from a JSON string
service_job_provider_instance = ServiceJobProvider.from_json(json)
# print the JSON string representation of the object
print(ServiceJobProvider.to_json())

# convert the object into a dict
service_job_provider_dict = service_job_provider_instance.to_dict()
# create an instance of ServiceJobProvider from a dict
service_job_provider_from_dict = ServiceJobProvider.from_dict(service_job_provider_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


