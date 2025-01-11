# LowestPriceType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition** | **str** | Indicates the condition of the item. For example: New, Used, Collectible, Refurbished, or Club. | 
**fulfillment_channel** | **str** | Indicates whether the item is fulfilled by Amazon or by the seller. | 
**offer_type** | [**OfferCustomerType**](OfferCustomerType.md) |  | [optional] 
**quantity_tier** | **int** | Indicates at what quantity this price becomes active. | [optional] 
**quantity_discount_type** | [**QuantityDiscountType**](QuantityDiscountType.md) |  | [optional] 
**landed_price** | [**MoneyType**](MoneyType.md) |  | [optional] 
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**shipping** | [**MoneyType**](MoneyType.md) |  | [optional] 
**points** | [**Points**](Points.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.lowest_price_type import LowestPriceType

# TODO update the JSON string below
json = "{}"
# create an instance of LowestPriceType from a JSON string
lowest_price_type_instance = LowestPriceType.from_json(json)
# print the JSON string representation of the object
print(LowestPriceType.to_json())

# convert the object into a dict
lowest_price_type_dict = lowest_price_type_instance.to_dict()
# create an instance of LowestPriceType from a dict
lowest_price_type_from_dict = LowestPriceType.from_dict(lowest_price_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


