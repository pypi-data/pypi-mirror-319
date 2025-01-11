# Offer

The offer data of a product.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_id** | **str** | The seller identifier for the offer. | 
**condition** | [**Condition**](Condition.md) |  | 
**sub_condition** | **str** | The item subcondition of the offer. | [optional] 
**fulfillment_type** | [**FulfillmentType**](FulfillmentType.md) |  | 
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**shipping_options** | [**List[ShippingOption]**](ShippingOption.md) | A list of shipping options associated with this offer | [optional] 
**points** | [**Points**](Points.md) |  | [optional] 
**prime_details** | [**PrimeDetails**](PrimeDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.offer import Offer

# TODO update the JSON string below
json = "{}"
# create an instance of Offer from a JSON string
offer_instance = Offer.from_json(json)
# print the JSON string representation of the object
print(Offer.to_json())

# convert the object into a dict
offer_dict = offer_instance.to_dict()
# create an instance of Offer from a dict
offer_from_dict = Offer.from_dict(offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


