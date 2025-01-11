# GetListingOffersBatchResponse

The response associated with the `getListingOffersBatch` API call.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**responses** | [**List[ListingOffersResponse]**](ListingOffersResponse.md) | A list of &#x60;getListingOffers&#x60; batched responses. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.get_listing_offers_batch_response import GetListingOffersBatchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetListingOffersBatchResponse from a JSON string
get_listing_offers_batch_response_instance = GetListingOffersBatchResponse.from_json(json)
# print the JSON string representation of the object
print(GetListingOffersBatchResponse.to_json())

# convert the object into a dict
get_listing_offers_batch_response_dict = get_listing_offers_batch_response_instance.to_dict()
# create an instance of GetListingOffersBatchResponse from a dict
get_listing_offers_batch_response_from_dict = GetListingOffersBatchResponse.from_dict(get_listing_offers_batch_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


