# BuyBoxPriceType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition** | **str** | Indicates the condition of the item. For example: New, Used, Collectible, Refurbished, or Club. | 
**offer_type** | [**OfferCustomerType**](OfferCustomerType.md) |  | [optional] 
**quantity_tier** | **int** | Indicates at what quantity this price becomes active. | [optional] 
**quantity_discount_type** | [**QuantityDiscountType**](QuantityDiscountType.md) |  | [optional] 
**landed_price** | [**MoneyType**](MoneyType.md) |  | 
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**shipping** | [**MoneyType**](MoneyType.md) |  | 
**points** | [**Points**](Points.md) |  | [optional] 
**seller_id** | **str** | The seller identifier for the offer. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.buy_box_price_type import BuyBoxPriceType

# TODO update the JSON string below
json = "{}"
# create an instance of BuyBoxPriceType from a JSON string
buy_box_price_type_instance = BuyBoxPriceType.from_json(json)
# print the JSON string representation of the object
print(BuyBoxPriceType.to_json())

# convert the object into a dict
buy_box_price_type_dict = buy_box_price_type_instance.to_dict()
# create an instance of BuyBoxPriceType from a dict
buy_box_price_type_from_dict = BuyBoxPriceType.from_dict(buy_box_price_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


