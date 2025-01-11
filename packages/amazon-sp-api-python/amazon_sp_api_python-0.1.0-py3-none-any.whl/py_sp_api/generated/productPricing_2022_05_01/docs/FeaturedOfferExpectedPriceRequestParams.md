# FeaturedOfferExpectedPriceRequestParams

The parameters for an individual request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace for which data is returned. | 
**sku** | **str** | The seller SKU of the item. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer_expected_price_request_params import FeaturedOfferExpectedPriceRequestParams

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOfferExpectedPriceRequestParams from a JSON string
featured_offer_expected_price_request_params_instance = FeaturedOfferExpectedPriceRequestParams.from_json(json)
# print the JSON string representation of the object
print(FeaturedOfferExpectedPriceRequestParams.to_json())

# convert the object into a dict
featured_offer_expected_price_request_params_dict = featured_offer_expected_price_request_params_instance.to_dict()
# create an instance of FeaturedOfferExpectedPriceRequestParams from a dict
featured_offer_expected_price_request_params_from_dict = FeaturedOfferExpectedPriceRequestParams.from_dict(featured_offer_expected_price_request_params_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


