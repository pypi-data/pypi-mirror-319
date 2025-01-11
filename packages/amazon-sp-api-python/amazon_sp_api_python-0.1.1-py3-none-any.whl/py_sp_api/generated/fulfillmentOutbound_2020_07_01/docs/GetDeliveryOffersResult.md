# GetDeliveryOffersResult

A list of delivery offers, including offer expiration, earliest and latest date and time range, and the delivery offer policy.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_offers** | [**List[DeliveryOffer]**](DeliveryOffer.md) | An array of delivery offer information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_delivery_offers_result import GetDeliveryOffersResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeliveryOffersResult from a JSON string
get_delivery_offers_result_instance = GetDeliveryOffersResult.from_json(json)
# print the JSON string representation of the object
print(GetDeliveryOffersResult.to_json())

# convert the object into a dict
get_delivery_offers_result_dict = get_delivery_offers_result_instance.to_dict()
# create an instance of GetDeliveryOffersResult from a dict
get_delivery_offers_result_from_dict = GetDeliveryOffersResult.from_dict(get_delivery_offers_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


