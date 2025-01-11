# GetDeliveryOffersTerms

The delivery terms for the delivery offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**origin** | [**Origin**](Origin.md) |  | 
**destination** | [**Destination**](Destination.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_delivery_offers_terms import GetDeliveryOffersTerms

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeliveryOffersTerms from a JSON string
get_delivery_offers_terms_instance = GetDeliveryOffersTerms.from_json(json)
# print the JSON string representation of the object
print(GetDeliveryOffersTerms.to_json())

# convert the object into a dict
get_delivery_offers_terms_dict = get_delivery_offers_terms_instance.to_dict()
# create an instance of GetDeliveryOffersTerms from a dict
get_delivery_offers_terms_from_dict = GetDeliveryOffersTerms.from_dict(get_delivery_offers_terms_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


