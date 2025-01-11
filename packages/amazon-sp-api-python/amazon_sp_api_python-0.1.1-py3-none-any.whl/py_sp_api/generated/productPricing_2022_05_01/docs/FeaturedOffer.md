# FeaturedOffer

Schema for `currentFeaturedOffer` or `competingFeaturedOffer`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**offer_identifier** | [**OfferIdentifier**](OfferIdentifier.md) |  | 
**condition** | [**Condition**](Condition.md) |  | [optional] 
**price** | [**Price**](Price.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer import FeaturedOffer

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOffer from a JSON string
featured_offer_instance = FeaturedOffer.from_json(json)
# print the JSON string representation of the object
print(FeaturedOffer.to_json())

# convert the object into a dict
featured_offer_dict = featured_offer_instance.to_dict()
# create an instance of FeaturedOffer from a dict
featured_offer_from_dict = FeaturedOffer.from_dict(featured_offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


