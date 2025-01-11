# ListingOffersResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | [**HttpResponseHeaders**](HttpResponseHeaders.md) |  | [optional] 
**status** | [**GetOffersHttpStatusLine**](GetOffersHttpStatusLine.md) |  | [optional] 
**body** | [**GetOffersResponse**](GetOffersResponse.md) |  | 
**request** | [**ListingOffersRequestParams**](ListingOffersRequestParams.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.listing_offers_response import ListingOffersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListingOffersResponse from a JSON string
listing_offers_response_instance = ListingOffersResponse.from_json(json)
# print the JSON string representation of the object
print(ListingOffersResponse.to_json())

# convert the object into a dict
listing_offers_response_dict = listing_offers_response_instance.to_dict()
# create an instance of ListingOffersResponse from a dict
listing_offers_response_from_dict = ListingOffersResponse.from_dict(listing_offers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


