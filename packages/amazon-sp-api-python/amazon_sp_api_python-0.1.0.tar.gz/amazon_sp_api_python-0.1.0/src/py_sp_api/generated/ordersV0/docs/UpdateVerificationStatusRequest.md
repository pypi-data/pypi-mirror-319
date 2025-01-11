# UpdateVerificationStatusRequest

The request body for the `updateVerificationStatus` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**regulated_order_verification_status** | [**UpdateVerificationStatusRequestBody**](UpdateVerificationStatusRequestBody.md) |  | 

## Example

```python
from py_sp_api.generated.ordersV0.models.update_verification_status_request import UpdateVerificationStatusRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateVerificationStatusRequest from a JSON string
update_verification_status_request_instance = UpdateVerificationStatusRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateVerificationStatusRequest.to_json())

# convert the object into a dict
update_verification_status_request_dict = update_verification_status_request_instance.to_dict()
# create an instance of UpdateVerificationStatusRequest from a dict
update_verification_status_request_from_dict = UpdateVerificationStatusRequest.from_dict(update_verification_status_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


