# GetDeliveryOffersRequest

The request body schema for the getDeliveryOffers operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product** | [**GetDeliveryOffersProduct**](GetDeliveryOffersProduct.md) |  | 
**terms** | [**GetDeliveryOffersTerms**](GetDeliveryOffersTerms.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_delivery_offers_request import GetDeliveryOffersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeliveryOffersRequest from a JSON string
get_delivery_offers_request_instance = GetDeliveryOffersRequest.from_json(json)
# print the JSON string representation of the object
print(GetDeliveryOffersRequest.to_json())

# convert the object into a dict
get_delivery_offers_request_dict = get_delivery_offers_request_instance.to_dict()
# create an instance of GetDeliveryOffersRequest from a dict
get_delivery_offers_request_from_dict = GetDeliveryOffersRequest.from_dict(get_delivery_offers_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


