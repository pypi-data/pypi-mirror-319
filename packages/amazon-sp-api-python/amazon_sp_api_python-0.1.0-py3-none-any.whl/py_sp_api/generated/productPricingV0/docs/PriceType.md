# PriceType


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**landed_price** | [**MoneyType**](MoneyType.md) |  | [optional] 
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**shipping** | [**MoneyType**](MoneyType.md) |  | [optional] 
**points** | [**Points**](Points.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.price_type import PriceType

# TODO update the JSON string below
json = "{}"
# create an instance of PriceType from a JSON string
price_type_instance = PriceType.from_json(json)
# print the JSON string representation of the object
print(PriceType.to_json())

# convert the object into a dict
price_type_dict = price_type_instance.to_dict()
# create an instance of PriceType from a dict
price_type_from_dict = PriceType.from_dict(price_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


