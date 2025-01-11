# FeaturedOfferExpectedPriceResponseBody

The FOEP response data for a requested SKU.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**offer_identifier** | [**OfferIdentifier**](OfferIdentifier.md) |  | [optional] 
**featured_offer_expected_price_results** | [**List[FeaturedOfferExpectedPriceResult]**](FeaturedOfferExpectedPriceResult.md) | A list of FOEP results for the requested offer. | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses that are returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer_expected_price_response_body import FeaturedOfferExpectedPriceResponseBody

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOfferExpectedPriceResponseBody from a JSON string
featured_offer_expected_price_response_body_instance = FeaturedOfferExpectedPriceResponseBody.from_json(json)
# print the JSON string representation of the object
print(FeaturedOfferExpectedPriceResponseBody.to_json())

# convert the object into a dict
featured_offer_expected_price_response_body_dict = featured_offer_expected_price_response_body_instance.to_dict()
# create an instance of FeaturedOfferExpectedPriceResponseBody from a dict
featured_offer_expected_price_response_body_from_dict = FeaturedOfferExpectedPriceResponseBody.from_dict(featured_offer_expected_price_response_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


