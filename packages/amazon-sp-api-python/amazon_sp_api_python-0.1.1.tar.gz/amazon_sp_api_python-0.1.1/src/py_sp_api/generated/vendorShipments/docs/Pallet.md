# Pallet

Details of the Pallet/Tare being shipped.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pallet_identifiers** | [**List[ContainerIdentification]**](ContainerIdentification.md) | A list of pallet identifiers. | 
**tier** | **int** | Number of layers per pallet. Only applicable to container type Pallet. | [optional] 
**block** | **int** | Number of cartons per layer on the pallet. Only applicable to container type Pallet. | [optional] 
**dimensions** | [**Dimensions**](Dimensions.md) |  | [optional] 
**weight** | [**Weight**](Weight.md) |  | [optional] 
**carton_reference_details** | [**CartonReferenceDetails**](CartonReferenceDetails.md) |  | [optional] 
**items** | [**List[ContainerItem]**](ContainerItem.md) | A list of container item details. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.pallet import Pallet

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


