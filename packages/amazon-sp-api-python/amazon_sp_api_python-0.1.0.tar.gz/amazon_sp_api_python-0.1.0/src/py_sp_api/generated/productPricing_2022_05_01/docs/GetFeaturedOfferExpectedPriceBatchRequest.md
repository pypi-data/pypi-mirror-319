# GetFeaturedOfferExpectedPriceBatchRequest

The request body for the `getFeaturedOfferExpectedPriceBatch` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**requests** | [**List[FeaturedOfferExpectedPriceRequest]**](FeaturedOfferExpectedPriceRequest.md) | A batched list of FOEP requests. | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.get_featured_offer_expected_price_batch_request import GetFeaturedOfferExpectedPriceBatchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetFeaturedOfferExpectedPriceBatchRequest from a JSON string
get_featured_offer_expected_price_batch_request_instance = GetFeaturedOfferExpectedPriceBatchRequest.from_json(json)
# print the JSON string representation of the object
print(GetFeaturedOfferExpectedPriceBatchRequest.to_json())

# convert the object into a dict
get_featured_offer_expected_price_batch_request_dict = get_featured_offer_expected_price_batch_request_instance.to_dict()
# create an instance of GetFeaturedOfferExpectedPriceBatchRequest from a dict
get_featured_offer_expected_price_batch_request_from_dict = GetFeaturedOfferExpectedPriceBatchRequest.from_dict(get_featured_offer_expected_price_batch_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


