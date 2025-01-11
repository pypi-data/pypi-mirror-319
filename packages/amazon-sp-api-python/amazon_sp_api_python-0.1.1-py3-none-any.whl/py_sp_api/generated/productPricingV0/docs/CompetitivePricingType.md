# CompetitivePricingType

Competitive pricing information for the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**competitive_prices** | [**List[CompetitivePriceType]**](CompetitivePriceType.md) | A list of competitive pricing information. | 
**number_of_offer_listings** | [**List[OfferListingCountType]**](OfferListingCountType.md) | The number of active offer listings for the item that was submitted. The listing count is returned by condition, one for each listing condition value that is returned. | 
**trade_in_value** | [**MoneyType**](MoneyType.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.competitive_pricing_type import CompetitivePricingType

# TODO update the JSON string below
json = "{}"
# create an instance of CompetitivePricingType from a JSON string
competitive_pricing_type_instance = CompetitivePricingType.from_json(json)
# print the JSON string representation of the object
print(CompetitivePricingType.to_json())

# convert the object into a dict
competitive_pricing_type_dict = competitive_pricing_type_instance.to_dict()
# create an instance of CompetitivePricingType from a dict
competitive_pricing_type_from_dict = CompetitivePricingType.from_dict(competitive_pricing_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


