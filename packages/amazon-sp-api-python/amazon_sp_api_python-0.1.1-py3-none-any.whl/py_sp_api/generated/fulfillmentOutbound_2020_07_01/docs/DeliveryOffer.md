# DeliveryOffer

An available offer for delivery of a product.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expires_at** | **datetime** | Date timestamp | [optional] 
**date_range** | [**DateRange**](DateRange.md) |  | [optional] 
**policy** | [**DeliveryPolicy**](DeliveryPolicy.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.delivery_offer import DeliveryOffer

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryOffer from a JSON string
delivery_offer_instance = DeliveryOffer.from_json(json)
# print the JSON string representation of the object
print(DeliveryOffer.to_json())

# convert the object into a dict
delivery_offer_dict = delivery_offer_instance.to_dict()
# create an instance of DeliveryOffer from a dict
delivery_offer_from_dict = DeliveryOffer.from_dict(delivery_offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


