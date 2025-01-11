# OfferType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**offer_type** | [**OfferCustomerType**](OfferCustomerType.md) |  | [optional] 
**buying_price** | [**PriceType**](PriceType.md) |  | 
**regular_price** | [**MoneyType**](MoneyType.md) |  | 
**business_price** | [**MoneyType**](MoneyType.md) |  | [optional] 
**quantity_discount_prices** | [**List[QuantityDiscountPriceType]**](QuantityDiscountPriceType.md) |  | [optional] 
**fulfillment_channel** | **str** | The fulfillment channel for the offer listing. Possible values:  * Amazon - Fulfilled by Amazon. * Merchant - Fulfilled by the seller. | 
**item_condition** | **str** | The item condition for the offer listing. Possible values: New, Used, Collectible, Refurbished, or Club. | 
**item_sub_condition** | **str** | The item subcondition for the offer listing. Possible values: New, Mint, Very Good, Good, Acceptable, Poor, Club, OEM, Warranty, Refurbished Warranty, Refurbished, Open Box, or Other. | 
**seller_sku** | **str** | The seller stock keeping unit (SKU) of the item. | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.offer_type import OfferType

# TODO update the JSON string below
json = "{}"
# create an instance of OfferType from a JSON string
offer_type_instance = OfferType.from_json(json)
# print the JSON string representation of the object
print(OfferType.to_json())

# convert the object into a dict
offer_type_dict = offer_type_instance.to_dict()
# create an instance of OfferType from a dict
offer_type_from_dict = OfferType.from_dict(offer_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


