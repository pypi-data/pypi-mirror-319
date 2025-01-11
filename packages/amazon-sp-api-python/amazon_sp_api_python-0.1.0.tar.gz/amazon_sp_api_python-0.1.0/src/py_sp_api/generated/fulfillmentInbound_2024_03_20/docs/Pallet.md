# Pallet

Contains information about a pallet that is used in the inbound plan. The pallet is a container that holds multiple items or boxes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**Dimensions**](Dimensions.md) |  | [optional] 
**package_id** | **str** | Primary key to uniquely identify a Package (Box or Pallet). | 
**quantity** | **int** | The number of containers where all other properties like weight or dimensions are identical. | [optional] 
**stackability** | [**Stackability**](Stackability.md) |  | [optional] 
**weight** | [**Weight**](Weight.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.pallet import Pallet

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


