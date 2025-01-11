# ChargeInstrument

A payment instrument.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | A short description of the charge instrument. | [optional] 
**tail** | **str** | The account tail (trailing digits) of the charge instrument. | [optional] 
**amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.charge_instrument import ChargeInstrument

# TODO update the JSON string below
json = "{}"
# create an instance of ChargeInstrument from a JSON string
charge_instrument_instance = ChargeInstrument.from_json(json)
# print the JSON string representation of the object
print(ChargeInstrument.to_json())

# convert the object into a dict
charge_instrument_dict = charge_instrument_instance.to_dict()
# create an instance of ChargeInstrument from a dict
charge_instrument_from_dict = ChargeInstrument.from_dict(charge_instrument_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


