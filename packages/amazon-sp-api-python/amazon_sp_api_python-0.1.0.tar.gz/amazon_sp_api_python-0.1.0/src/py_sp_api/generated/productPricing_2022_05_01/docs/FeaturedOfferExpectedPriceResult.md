# FeaturedOfferExpectedPriceResult

The FOEP result data for the requested offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**featured_offer_expected_price** | [**FeaturedOfferExpectedPrice**](FeaturedOfferExpectedPrice.md) |  | [optional] 
**result_status** | **str** | The status of the FOEP computation. Possible values include &#x60;VALID_FOEP&#x60;, &#x60;NO_COMPETING_OFFER&#x60;, &#x60;OFFER_NOT_ELIGIBLE&#x60;, &#x60;OFFER_NOT_FOUND&#x60;, and &#x60;ASIN_NOT_ELIGIBLE&#x60;. Additional values might be added in the future. | 
**competing_featured_offer** | [**FeaturedOffer**](FeaturedOffer.md) |  | [optional] 
**current_featured_offer** | [**FeaturedOffer**](FeaturedOffer.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer_expected_price_result import FeaturedOfferExpectedPriceResult

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOfferExpectedPriceResult from a JSON string
featured_offer_expected_price_result_instance = FeaturedOfferExpectedPriceResult.from_json(json)
# print the JSON string representation of the object
print(FeaturedOfferExpectedPriceResult.to_json())

# convert the object into a dict
featured_offer_expected_price_result_dict = featured_offer_expected_price_result_instance.to_dict()
# create an instance of FeaturedOfferExpectedPriceResult from a dict
featured_offer_expected_price_result_from_dict = FeaturedOfferExpectedPriceResult.from_dict(featured_offer_expected_price_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


