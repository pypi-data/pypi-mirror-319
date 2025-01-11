# GetDeliveryOffersResponse

The response schema for the getDeliveryOffers operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetDeliveryOffersResult**](GetDeliveryOffersResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_delivery_offers_response import GetDeliveryOffersResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeliveryOffersResponse from a JSON string
get_delivery_offers_response_instance = GetDeliveryOffersResponse.from_json(json)
# print the JSON string representation of the object
print(GetDeliveryOffersResponse.to_json())

# convert the object into a dict
get_delivery_offers_response_dict = get_delivery_offers_response_instance.to_dict()
# create an instance of GetDeliveryOffersResponse from a dict
get_delivery_offers_response_from_dict = GetDeliveryOffersResponse.from_dict(get_delivery_offers_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


