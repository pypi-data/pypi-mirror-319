# Summary

Contains price information about the product, including the LowestPrices and BuyBoxPrices, the ListPrice, the SuggestedLowerPricePlusShipping, and NumberOfOffers and NumberOfBuyBoxEligibleOffers.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_offer_count** | **int** | The number of unique offers contained in NumberOfOffers. | 
**number_of_offers** | [**List[OfferCountType]**](OfferCountType.md) |  | [optional] 
**lowest_prices** | [**List[LowestPriceType]**](LowestPriceType.md) |  | [optional] 
**buy_box_prices** | [**List[BuyBoxPriceType]**](BuyBoxPriceType.md) |  | [optional] 
**list_price** | [**MoneyType**](MoneyType.md) |  | [optional] 
**competitive_price_threshold** | [**MoneyType**](MoneyType.md) |  | [optional] 
**suggested_lower_price_plus_shipping** | [**MoneyType**](MoneyType.md) |  | [optional] 
**sales_rankings** | [**List[SalesRankType]**](SalesRankType.md) | A list of sales rank information for the item, by category. | [optional] 
**buy_box_eligible_offers** | [**List[OfferCountType]**](OfferCountType.md) |  | [optional] 
**offers_available_time** | **datetime** | When the status is ActiveButTooSoonForProcessing, this is the time when the offers will be available for processing. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.summary import Summary

# TODO update the JSON string below
json = "{}"
# create an instance of Summary from a JSON string
summary_instance = Summary.from_json(json)
# print the JSON string representation of the object
print(Summary.to_json())

# convert the object into a dict
summary_dict = summary_instance.to_dict()
# create an instance of Summary from a dict
summary_from_dict = Summary.from_dict(summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


