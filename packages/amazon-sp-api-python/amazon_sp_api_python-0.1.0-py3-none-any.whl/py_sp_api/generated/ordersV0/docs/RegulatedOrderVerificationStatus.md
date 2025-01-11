# RegulatedOrderVerificationStatus

The verification status of the order, along with associated approval or rejection metadata.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**VerificationStatus**](VerificationStatus.md) |  | 
**requires_merchant_action** | **bool** | When true, the regulated information provided in the order requires a review by the merchant. | 
**valid_rejection_reasons** | [**List[RejectionReason]**](RejectionReason.md) | A list of valid rejection reasons that may be used to reject the order&#39;s regulated information. | 
**rejection_reason** | [**RejectionReason**](RejectionReason.md) |  | [optional] 
**review_date** | **str** | The date the order was reviewed. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date time format. | [optional] 
**external_reviewer_id** | **str** | The identifier for the order&#39;s regulated information reviewer. | [optional] 
**valid_verification_details** | [**List[ValidVerificationDetail]**](ValidVerificationDetail.md) | A list of valid verification details that may be provided and the criteria required for when the verification detail can be provided. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.regulated_order_verification_status import RegulatedOrderVerificationStatus

# TODO update the JSON string below
json = "{}"
# create an instance of RegulatedOrderVerificationStatus from a JSON string
regulated_order_verification_status_instance = RegulatedOrderVerificationStatus.from_json(json)
# print the JSON string representation of the object
print(RegulatedOrderVerificationStatus.to_json())

# convert the object into a dict
regulated_order_verification_status_dict = regulated_order_verification_status_instance.to_dict()
# create an instance of RegulatedOrderVerificationStatus from a dict
regulated_order_verification_status_from_dict = RegulatedOrderVerificationStatus.from_dict(regulated_order_verification_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


