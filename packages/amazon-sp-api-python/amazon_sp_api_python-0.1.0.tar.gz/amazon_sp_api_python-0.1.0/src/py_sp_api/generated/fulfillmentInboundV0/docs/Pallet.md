# Pallet

Pallet information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**weight** | [**Weight**](Weight.md) |  | [optional] 
**is_stacked** | **bool** | Indicates whether pallets will be stacked when carrier arrives for pick-up. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.pallet import Pallet

# TODO update the JSON string below
json = "{}"
# create an instance of Pallet from a JSON string
pallet_instance = Pallet.from_json(json)
# print the JSON string representation of the object
print(Pallet.to_json())

# convert the object into a dict
pallet_dict = pallet_instance.to_dict()
# create an instance of Pallet from a dict
pallet_from_dict = Pallet.from_dict(pallet_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


