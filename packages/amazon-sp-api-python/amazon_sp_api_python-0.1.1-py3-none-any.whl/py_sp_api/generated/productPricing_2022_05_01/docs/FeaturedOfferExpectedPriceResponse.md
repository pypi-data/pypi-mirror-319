# FeaturedOfferExpectedPriceResponse

Schema for an individual FOEP response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | **Dict[str, str]** | A mapping of additional HTTP headers to send or receive for an individual request within a batch. | 
**status** | [**HttpStatusLine**](HttpStatusLine.md) |  | 
**request** | [**FeaturedOfferExpectedPriceRequestParams**](FeaturedOfferExpectedPriceRequestParams.md) |  | 
**body** | [**FeaturedOfferExpectedPriceResponseBody**](FeaturedOfferExpectedPriceResponseBody.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer_expected_price_response import FeaturedOfferExpectedPriceResponse

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOfferExpectedPriceResponse from a JSON string
featured_offer_expected_price_response_instance = FeaturedOfferExpectedPriceResponse.from_json(json)
# print the JSON string representation of the object
print(FeaturedOfferExpectedPriceResponse.to_json())

# convert the object into a dict
featured_offer_expected_price_response_dict = featured_offer_expected_price_response_instance.to_dict()
# create an instance of FeaturedOfferExpectedPriceResponse from a dict
featured_offer_expected_price_response_from_dict = FeaturedOfferExpectedPriceResponse.from_dict(featured_offer_expected_price_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


