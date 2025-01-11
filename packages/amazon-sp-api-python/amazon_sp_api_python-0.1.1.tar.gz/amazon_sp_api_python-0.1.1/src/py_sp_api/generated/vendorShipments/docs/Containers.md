# Containers

A list of the items in this transportation and their associated inner container details. If any of the item detail fields are common at a carton or a pallet level, provide them at the corresponding carton or pallet level.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_type** | **str** | The type of container. | 
**container_sequence_number** | **str** | An integer that must be submitted for multi-box shipments only, where one item may come in separate packages. | [optional] 
**container_identifiers** | [**List[ContainerIdentification]**](ContainerIdentification.md) | A list of carton identifiers. | 
**tracking_number** | **str** | The tracking number used for identifying the shipment. | [optional] 
**dimensions** | [**Dimensions**](Dimensions.md) |  | [optional] 
**weight** | [**Weight**](Weight.md) |  | [optional] 
**tier** | **int** | Number of layers per pallet. | [optional] 
**block** | **int** | Number of cartons per layer on the pallet. | [optional] 
**inner_containers_details** | [**InnerContainersDetails**](InnerContainersDetails.md) |  | [optional] 
**packed_items** | [**List[PackedItems]**](PackedItems.md) | A list of packed items. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.containers import Containers

# TODO update the JSON string below
json = "{}"
# create an instance of Containers from a JSON string
containers_instance = Containers.from_json(json)
# print the JSON string representation of the object
print(Containers.to_json())

# convert the object into a dict
containers_dict = containers_instance.to_dict()
# create an instance of Containers from a dict
containers_from_dict = Containers.from_dict(containers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


