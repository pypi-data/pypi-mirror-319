# PalletInput

Contains input information about a pallet to be used in the inbound plan.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**Dimensions**](Dimensions.md) |  | [optional] 
**quantity** | **int** | The number of containers where all other properties like weight or dimensions are identical. | 
**stackability** | [**Stackability**](Stackability.md) |  | [optional] 
**weight** | [**Weight**](Weight.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.pallet_input import PalletInput

# TODO update the JSON string below
json = "{}"
# create an instance of PalletInput from a JSON string
pallet_input_instance = PalletInput.from_json(json)
# print the JSON string representation of the object
print(PalletInput.to_json())

# convert the object into a dict
pallet_input_dict = pallet_input_instance.to_dict()
# create an instance of PalletInput from a dict
pallet_input_from_dict = PalletInput.from_dict(pallet_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


