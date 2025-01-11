# GetItemOffersBatchResponse

The response associated with the `getItemOffersBatch` API call.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**responses** | [**List[ItemOffersResponse]**](ItemOffersResponse.md) | A list of &#x60;getItemOffers&#x60; batched responses. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.get_item_offers_batch_response import GetItemOffersBatchResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetItemOffersBatchResponse from a JSON string
get_item_offers_batch_response_instance = GetItemOffersBatchResponse.from_json(json)
# print the JSON string representation of the object
print(GetItemOffersBatchResponse.to_json())

# convert the object into a dict
get_item_offers_batch_response_dict = get_item_offers_batch_response_instance.to_dict()
# create an instance of GetItemOffersBatchResponse from a dict
get_item_offers_batch_response_from_dict = GetItemOffersBatchResponse.from_dict(get_item_offers_batch_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


