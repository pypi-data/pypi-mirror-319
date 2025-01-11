# QuantityDiscountPriceType

Contains pricing information that includes special pricing when buying in bulk.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**quantity_tier** | **int** | Indicates at what quantity this price becomes active. | 
**quantity_discount_type** | [**QuantityDiscountType**](QuantityDiscountType.md) |  | 
**listing_price** | [**MoneyType**](MoneyType.md) |  | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.quantity_discount_price_type import QuantityDiscountPriceType

# TODO update the JSON string below
json = "{}"
# create an instance of QuantityDiscountPriceType from a JSON string
quantity_discount_price_type_instance = QuantityDiscountPriceType.from_json(json)
# print the JSON string representation of the object
print(QuantityDiscountPriceType.to_json())

# convert the object into a dict
quantity_discount_price_type_dict = quantity_discount_price_type_instance.to_dict()
# create an instance of QuantityDiscountPriceType from a dict
quantity_discount_price_type_from_dict = QuantityDiscountPriceType.from_dict(quantity_discount_price_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


