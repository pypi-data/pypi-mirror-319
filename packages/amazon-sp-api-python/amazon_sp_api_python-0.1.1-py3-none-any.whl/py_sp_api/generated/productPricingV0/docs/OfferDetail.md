# OfferDetail


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**my_offer** | **bool** | When true, this is the seller&#39;s offer. | [optional] 
**offer_type** | [**OfferCustomerType**](OfferCustomerType.md) |  | [optional] 
**sub_condition** | **str** | The subcondition of the item. Subcondition values: New, Mint, Very Good, Good, Acceptable, Poor, Club, OEM, Warranty, Refurbished Warranty, Refurbished, Open Box, or Other. | 
**seller_id** | **str** | The seller identifier for the offer. | [optional] 
**condition_notes** | **str** | Information about the condition of the item. | [optional] 
**seller_feedback_rating** | [**SellerFeedbackType**](SellerFeedbackType.md) |  | [optional] 
**shipping_time** | [**DetailedShippingTimeType**](DetailedShippingTimeType.md) |  | 
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**quantity_discount_prices** | [**List[QuantityDiscountPriceType]**](QuantityDiscountPriceType.md) |  | [optional] 
**points** | [**Points**](Points.md) |  | [optional] 
**shipping** | [**MoneyType**](MoneyType.md) |  | 
**ships_from** | [**ShipsFromType**](ShipsFromType.md) |  | [optional] 
**is_fulfilled_by_amazon** | **bool** | When true, the offer is fulfilled by Amazon. | 
**prime_information** | [**PrimeInformationType**](PrimeInformationType.md) |  | [optional] 
**is_buy_box_winner** | **bool** | When true, the offer is currently in the Buy Box. There can be up to two Buy Box winners at any time per ASIN, one that is eligible for Prime and one that is not eligible for Prime. | [optional] 
**is_featured_merchant** | **bool** | When true, the seller of the item is eligible to win the Buy Box. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.offer_detail import OfferDetail

# TODO update the JSON string below
json = "{}"
# create an instance of OfferDetail from a JSON string
offer_detail_instance = OfferDetail.from_json(json)
# print the JSON string representation of the object
print(OfferDetail.to_json())

# convert the object into a dict
offer_detail_dict = offer_detail_instance.to_dict()
# create an instance of OfferDetail from a dict
offer_detail_from_dict = OfferDetail.from_dict(offer_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


