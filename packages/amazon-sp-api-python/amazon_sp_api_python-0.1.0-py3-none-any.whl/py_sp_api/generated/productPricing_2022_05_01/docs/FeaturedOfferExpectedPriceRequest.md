# FeaturedOfferExpectedPriceRequest

An individual FOEP request for a particular SKU.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uri** | **str** | The URI associated with an individual request within a batch. For &#x60;FeaturedOfferExpectedPrice&#x60;, this is &#x60;/products/pricing/2022-05-01/offer/featuredOfferExpectedPrice&#x60;. | 
**method** | [**HttpMethod**](HttpMethod.md) |  | 
**body** | **Dict[str, object]** | Additional HTTP body information that is associated with an individual request within a batch. | [optional] 
**headers** | **Dict[str, str]** | A mapping of additional HTTP headers to send or receive for an individual request within a batch. | [optional] 
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace for which data is returned. | 
**sku** | **str** | The seller SKU of the item. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer_expected_price_request import FeaturedOfferExpectedPriceRequest

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOfferExpectedPriceRequest from a JSON string
featured_offer_expected_price_request_instance = FeaturedOfferExpectedPriceRequest.from_json(json)
# print the JSON string representation of the object
print(FeaturedOfferExpectedPriceRequest.to_json())

# convert the object into a dict
featured_offer_expected_price_request_dict = featured_offer_expected_price_request_instance.to_dict()
# create an instance of FeaturedOfferExpectedPriceRequest from a dict
featured_offer_expected_price_request_from_dict = FeaturedOfferExpectedPriceRequest.from_dict(featured_offer_expected_price_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


