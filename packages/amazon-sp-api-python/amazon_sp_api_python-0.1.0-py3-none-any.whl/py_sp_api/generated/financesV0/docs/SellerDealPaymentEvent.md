# SellerDealPaymentEvent

An event linked to the payment of a fee related to the specified deal.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**deal_id** | **str** | The unique identifier of the deal. | [optional] 
**deal_description** | **str** | The internal description of the deal. | [optional] 
**event_type** | **str** | The type of event: SellerDealComplete. | [optional] 
**fee_type** | **str** | The type of fee: RunLightningDealFee. | [optional] 
**fee_amount** | [**Currency**](Currency.md) |  | [optional] 
**tax_amount** | [**Currency**](Currency.md) |  | [optional] 
**total_amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.seller_deal_payment_event import SellerDealPaymentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of SellerDealPaymentEvent from a JSON string
seller_deal_payment_event_instance = SellerDealPaymentEvent.from_json(json)
# print the JSON string representation of the object
print(SellerDealPaymentEvent.to_json())

# convert the object into a dict
seller_deal_payment_event_dict = seller_deal_payment_event_instance.to_dict()
# create an instance of SellerDealPaymentEvent from a dict
seller_deal_payment_event_from_dict = SellerDealPaymentEvent.from_dict(seller_deal_payment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


