# GetListingOffersBatchRequest

The request associated with the `getListingOffersBatch` API call.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**requests** | [**List[ListingOffersRequest]**](ListingOffersRequest.md) | A list of &#x60;getListingOffers&#x60; batched requests to run. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.get_listing_offers_batch_request import GetListingOffersBatchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetListingOffersBatchRequest from a JSON string
get_listing_offers_batch_request_instance = GetListingOffersBatchRequest.from_json(json)
# print the JSON string representation of the object
print(GetListingOffersBatchRequest.to_json())

# convert the object into a dict
get_listing_offers_batch_request_dict = get_listing_offers_batch_request_instance.to_dict()
# create an instance of GetListingOffersBatchRequest from a dict
get_listing_offers_batch_request_from_dict = GetListingOffersBatchRequest.from_dict(get_listing_offers_batch_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


