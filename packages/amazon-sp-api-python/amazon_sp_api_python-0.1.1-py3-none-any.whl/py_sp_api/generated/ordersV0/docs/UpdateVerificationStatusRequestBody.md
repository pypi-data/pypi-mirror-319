# UpdateVerificationStatusRequestBody

The updated values of the `VerificationStatus` field.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**VerificationStatus**](VerificationStatus.md) |  | [optional] 
**external_reviewer_id** | **str** | The identifier of the order&#39;s regulated information reviewer. | 
**rejection_reason_id** | **str** | The unique identifier of the rejection reason used for rejecting the order&#39;s regulated information. Only required if the new status is rejected. | [optional] 
**verification_details** | [**VerificationDetails**](VerificationDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.update_verification_status_request_body import UpdateVerificationStatusRequestBody

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateVerificationStatusRequestBody from a JSON string
update_verification_status_request_body_instance = UpdateVerificationStatusRequestBody.from_json(json)
# print the JSON string representation of the object
print(UpdateVerificationStatusRequestBody.to_json())

# convert the object into a dict
update_verification_status_request_body_dict = update_verification_status_request_body_instance.to_dict()
# create an instance of UpdateVerificationStatusRequestBody from a dict
update_verification_status_request_body_from_dict = UpdateVerificationStatusRequestBody.from_dict(update_verification_status_request_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


