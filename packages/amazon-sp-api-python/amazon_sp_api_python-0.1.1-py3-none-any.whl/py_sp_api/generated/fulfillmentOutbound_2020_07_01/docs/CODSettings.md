# CODSettings

The COD (Cash On Delivery) charges that you associate with a COD fulfillment order.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_cod_required** | **bool** | When true, this fulfillment order requires a COD (Cash On Delivery) payment. | 
**cod_charge** | [**Money**](Money.md) |  | [optional] 
**cod_charge_tax** | [**Money**](Money.md) |  | [optional] 
**shipping_charge** | [**Money**](Money.md) |  | [optional] 
**shipping_charge_tax** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.cod_settings import CODSettings

# TODO update the JSON string below
json = "{}"
# create an instance of CODSettings from a JSON string
cod_settings_instance = CODSettings.from_json(json)
# print the JSON string representation of the object
print(CODSettings.to_json())

# convert the object into a dict
cod_settings_dict = cod_settings_instance.to_dict()
# create an instance of CODSettings from a dict
cod_settings_from_dict = CODSettings.from_dict(cod_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


