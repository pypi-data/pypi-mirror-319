# Container

A container used for shipping and packing items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_type** | **str** | The type of container. | 
**container_identifier** | **str** | The container identifier. | 
**tracking_number** | **str** | The tracking number. | [optional] 
**manifest_id** | **str** | The manifest identifier. | [optional] 
**manifest_date** | **str** | The date of the manifest. | [optional] 
**ship_method** | **str** | The shipment method. | [optional] 
**scac_code** | **str** | SCAC code required for NA VOC vendors only. | [optional] 
**carrier** | **str** | Carrier required for EU VOC vendors only. | [optional] 
**container_sequence_number** | **int** | An integer that must be submitted for multi-box shipments only, where one item may come in separate packages. | [optional] 
**dimensions** | [**Dimensions**](Dimensions.md) |  | [optional] 
**weight** | [**Weight**](Weight.md) |  | 
**packed_items** | [**List[PackedItem]**](PackedItem.md) | A list of packed items. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShippingV1.models.container import Container

# TODO update the JSON string below
json = "{}"
# create an instance of Container from a JSON string
container_instance = Container.from_json(json)
# print the JSON string representation of the object
print(Container.to_json())

# convert the object into a dict
container_dict = container_instance.to_dict()
# create an instance of Container from a dict
container_from_dict = Container.from_dict(container_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


