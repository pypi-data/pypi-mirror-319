# GetFeaturedOfferExpectedPriceBatchResponse

The response schema for the `getFeaturedOfferExpectedPriceBatch` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**responses** | [**List[FeaturedOfferExpectedPriceResponse]**](FeaturedOfferExpectedPriceResponse.md) | A batched list of FOEP responses. | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.get_featured_offer_expected_price_batch_response import GetFeaturedOfferExpectedPriceBatchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeaturedOfferExpectedPriceBatchResponse from a JSON string
get_featured_offer_expected_price_batch_response_instance = GetFeaturedOfferExpectedPriceBatchResponse.from_json(json)
# print the JSON string representation of the object
print(GetFeaturedOfferExpectedPriceBatchResponse.to_json())

# convert the object into a dict
get_featured_offer_expected_price_batch_response_dict = get_featured_offer_expected_price_batch_response_instance.to_dict()
# create an instance of GetFeaturedOfferExpectedPriceBatchResponse from a dict
get_featured_offer_expected_price_batch_response_from_dict = GetFeaturedOfferExpectedPriceBatchResponse.from_dict(get_featured_offer_expected_price_batch_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


