# GetDeliveryOffersProduct

The product details for the delivery offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_identifier** | [**ProductIdentifier**](ProductIdentifier.md) |  | 
**amount** | [**Amount**](Amount.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_delivery_offers_product import GetDeliveryOffersProduct

# TODO update the JSON string below
json = "{}"
# create an instance of GetDeliveryOffersProduct from a JSON string
get_delivery_offers_product_instance = GetDeliveryOffersProduct.from_json(json)
# print the JSON string representation of the object
print(GetDeliveryOffersProduct.to_json())

# convert the object into a dict
get_delivery_offers_product_dict = get_delivery_offers_product_instance.to_dict()
# create an instance of GetDeliveryOffersProduct from a dict
get_delivery_offers_product_from_dict = GetDeliveryOffersProduct.from_dict(get_delivery_offers_product_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


