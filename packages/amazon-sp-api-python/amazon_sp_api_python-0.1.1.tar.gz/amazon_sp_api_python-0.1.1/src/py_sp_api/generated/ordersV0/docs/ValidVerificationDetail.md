# ValidVerificationDetail

The types of verification details that may be provided for the order and the criteria required for when the type of verification detail can be provided. The types of verification details allowed depend on the type of regulated product and will not change order to order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**verification_detail_type** | **str** | A supported type of verification detail. The type indicates which verification detail could be shared while updating the regulated order. Valid value: &#x60;prescriptionDetail&#x60;. | 
**valid_verification_statuses** | [**List[VerificationStatus]**](VerificationStatus.md) | A list of valid verification statuses where the associated verification detail type may be provided. For example, if the value of this field is [\&quot;Approved\&quot;], calls to provide the associated verification detail will fail for orders with a &#x60;VerificationStatus&#x60; of &#x60;Pending&#x60;, &#x60;Rejected&#x60;, &#x60;Expired&#x60;, or &#x60;Cancelled&#x60;. | 

## Example

```python
from py_sp_api.generated.ordersV0.models.valid_verification_detail import ValidVerificationDetail

# TODO update the JSON string below
json = "{}"
# create an instance of ValidVerificationDetail from a JSON string
valid_verification_detail_instance = ValidVerificationDetail.from_json(json)
# print the JSON string representation of the object
print(ValidVerificationDetail.to_json())

# convert the object into a dict
valid_verification_detail_dict = valid_verification_detail_instance.to_dict()
# create an instance of ValidVerificationDetail from a dict
valid_verification_detail_from_dict = ValidVerificationDetail.from_dict(valid_verification_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


