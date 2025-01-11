# CompetitivePriceType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**competitive_price_id** | **str** | The pricing model for each price that is returned.  Possible values:  * 1 - New Buy Box Price. * 2 - Used Buy Box Price. | 
**price** | [**PriceType**](PriceType.md) |  | 
**condition** | **str** | Indicates the condition of the item whose pricing information is returned. Possible values are: New, Used, Collectible, Refurbished, or Club. | [optional] 
**subcondition** | **str** | Indicates the subcondition of the item whose pricing information is returned. Possible values are: New, Mint, Very Good, Good, Acceptable, Poor, Club, OEM, Warranty, Refurbished Warranty, Refurbished, Open Box, or Other. | [optional] 
**offer_type** | [**OfferCustomerType**](OfferCustomerType.md) |  | [optional] 
**quantity_tier** | **int** | Indicates at what quantity this price becomes active. | [optional] 
**quantity_discount_type** | [**QuantityDiscountType**](QuantityDiscountType.md) |  | [optional] 
**seller_id** | **str** | The seller identifier for the offer. | [optional] 
**belongs_to_requester** | **bool** |  Indicates whether or not the pricing information is for an offer listing that belongs to the requester. The requester is the seller associated with the SellerId that was submitted with the request. Possible values are: true and false. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.competitive_price_type import CompetitivePriceType

# TODO update the JSON string below
json = "{}"
# create an instance of CompetitivePriceType from a JSON string
competitive_price_type_instance = CompetitivePriceType.from_json(json)
# print the JSON string representation of the object
print(CompetitivePriceType.to_json())

# convert the object into a dict
competitive_price_type_dict = competitive_price_type_instance.to_dict()
# create an instance of CompetitivePriceType from a dict
competitive_price_type_from_dict = CompetitivePriceType.from_dict(competitive_price_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


