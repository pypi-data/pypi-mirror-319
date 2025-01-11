# ShippingOption

The shipping option available for the offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_option_type** | **str** | The type of shipping option. | 
**price** | [**MoneyType**](MoneyType.md) |  | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.shipping_option import ShippingOption

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingOption from a JSON string
shipping_option_instance = ShippingOption.from_json(json)
# print the JSON string representation of the object
print(ShippingOption.to_json())

# convert the object into a dict
shipping_option_dict = shipping_option_instance.to_dict()
# create an instance of ShippingOption from a dict
shipping_option_from_dict = ShippingOption.from_dict(shipping_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


