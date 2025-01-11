# FeaturedOfferExpectedPrice

The item price at or below which the target offer may be featured.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**points** | [**Points**](Points.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer_expected_price import FeaturedOfferExpectedPrice

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOfferExpectedPrice from a JSON string
featured_offer_expected_price_instance = FeaturedOfferExpectedPrice.from_json(json)
# print the JSON string representation of the object
print(FeaturedOfferExpectedPrice.to_json())

# convert the object into a dict
featured_offer_expected_price_dict = featured_offer_expected_price_instance.to_dict()
# create an instance of FeaturedOfferExpectedPrice from a dict
featured_offer_expected_price_from_dict = FeaturedOfferExpectedPrice.from_dict(featured_offer_expected_price_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


