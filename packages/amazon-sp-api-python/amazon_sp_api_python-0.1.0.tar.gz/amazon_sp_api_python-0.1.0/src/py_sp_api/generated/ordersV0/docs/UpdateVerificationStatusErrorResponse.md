# UpdateVerificationStatusErrorResponse

The error response schema for the `UpdateVerificationStatus` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.update_verification_status_error_response import UpdateVerificationStatusErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateVerificationStatusErrorResponse from a JSON string
update_verification_status_error_response_instance = UpdateVerificationStatusErrorResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateVerificationStatusErrorResponse.to_json())

# convert the object into a dict
update_verification_status_error_response_dict = update_verification_status_error_response_instance.to_dict()
# create an instance of UpdateVerificationStatusErrorResponse from a dict
update_verification_status_error_response_from_dict = UpdateVerificationStatusErrorResponse.from_dict(update_verification_status_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


