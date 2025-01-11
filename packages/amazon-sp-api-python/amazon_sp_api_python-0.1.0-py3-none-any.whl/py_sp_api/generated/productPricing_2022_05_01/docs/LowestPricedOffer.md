# LowestPricedOffer

Describes the lowest priced offers for the specified item condition and offer type.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**lowest_priced_offers_input** | [**LowestPricedOffersInput**](LowestPricedOffersInput.md) |  | 
**offers** | [**List[Offer]**](Offer.md) | A list of up to 20 lowest priced offers that match the criteria specified in &#x60;lowestPricedOffersInput&#x60;. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.lowest_priced_offer import LowestPricedOffer

# TODO update the JSON string below
json = "{}"
# create an instance of LowestPricedOffer from a JSON string
lowest_priced_offer_instance = LowestPricedOffer.from_json(json)
# print the JSON string representation of the object
print(LowestPricedOffer.to_json())

# convert the object into a dict
lowest_priced_offer_dict = lowest_priced_offer_instance.to_dict()
# create an instance of LowestPricedOffer from a dict
lowest_priced_offer_from_dict = LowestPricedOffer.from_dict(lowest_priced_offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


