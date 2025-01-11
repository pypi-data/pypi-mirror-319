# GetItemOffersBatchRequest

The request associated with the `getItemOffersBatch` API call.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**requests** | [**List[ItemOffersRequest]**](ItemOffersRequest.md) | A list of &#x60;getListingOffers&#x60; batched requests to run. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.get_item_offers_batch_request import GetItemOffersBatchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetItemOffersBatchRequest from a JSON string
get_item_offers_batch_request_instance = GetItemOffersBatchRequest.from_json(json)
# print the JSON string representation of the object
print(GetItemOffersBatchRequest.to_json())

# convert the object into a dict
get_item_offers_batch_request_dict = get_item_offers_batch_request_instance.to_dict()
# create an instance of GetItemOffersBatchRequest from a dict
get_item_offers_batch_request_from_dict = GetItemOffersBatchRequest.from_dict(get_item_offers_batch_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


