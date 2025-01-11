# CreateConfirmServiceDetailsResponse

The response schema for the createConfirmServiceDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.messaging.models.create_confirm_service_details_response import CreateConfirmServiceDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateConfirmServiceDetailsResponse from a JSON string
create_confirm_service_details_response_instance = CreateConfirmServiceDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(CreateConfirmServiceDetailsResponse.to_json())

# convert the object into a dict
create_confirm_service_details_response_dict = create_confirm_service_details_response_instance.to_dict()
# create an instance of CreateConfirmServiceDetailsResponse from a dict
create_confirm_service_details_response_from_dict = CreateConfirmServiceDetailsResponse.from_dict(create_confirm_service_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


