# SellerReviewEnrollmentPaymentEvent

A fee payment event for the Early Reviewer Program.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**enrollment_id** | **str** | An enrollment identifier. | [optional] 
**parent_asin** | **str** | The Amazon Standard Identification Number (ASIN) of the item that was enrolled in the Early Reviewer Program. | [optional] 
**fee_component** | [**FeeComponent**](FeeComponent.md) |  | [optional] 
**charge_component** | [**ChargeComponent**](ChargeComponent.md) |  | [optional] 
**total_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.seller_review_enrollment_payment_event import SellerReviewEnrollmentPaymentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of SellerReviewEnrollmentPaymentEvent from a JSON string
seller_review_enrollment_payment_event_instance = SellerReviewEnrollmentPaymentEvent.from_json(json)
# print the JSON string representation of the object
print(SellerReviewEnrollmentPaymentEvent.to_json())

# convert the object into a dict
seller_review_enrollment_payment_event_dict = seller_review_enrollment_payment_event_instance.to_dict()
# create an instance of SellerReviewEnrollmentPaymentEvent from a dict
seller_review_enrollment_payment_event_from_dict = SellerReviewEnrollmentPaymentEvent.from_dict(seller_review_enrollment_payment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


