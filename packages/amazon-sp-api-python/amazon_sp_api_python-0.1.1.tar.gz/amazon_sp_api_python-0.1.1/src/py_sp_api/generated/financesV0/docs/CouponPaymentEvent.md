# CouponPaymentEvent

An event related to coupon payments.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**coupon_id** | **str** | A coupon identifier. | [optional] 
**seller_coupon_description** | **str** | The description provided by the seller when they created the coupon. | [optional] 
**clip_or_redemption_count** | **int** | The number of coupon clips or redemptions. | [optional] 
**payment_event_id** | **str** | A payment event identifier. | [optional] 
**fee_component** | [**FeeComponent**](FeeComponent.md) |  | [optional] 
**charge_component** | [**ChargeComponent**](ChargeComponent.md) |  | [optional] 
**total_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.coupon_payment_event import CouponPaymentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of CouponPaymentEvent from a JSON string
coupon_payment_event_instance = CouponPaymentEvent.from_json(json)
# print the JSON string representation of the object
print(CouponPaymentEvent.to_json())

# convert the object into a dict
coupon_payment_event_dict = coupon_payment_event_instance.to_dict()
# create an instance of CouponPaymentEvent from a dict
coupon_payment_event_from_dict = CouponPaymentEvent.from_dict(coupon_payment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


