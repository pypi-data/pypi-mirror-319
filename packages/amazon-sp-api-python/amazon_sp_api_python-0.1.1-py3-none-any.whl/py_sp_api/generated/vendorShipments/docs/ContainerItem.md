# ContainerItem

Carton/Pallet level details for the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item_reference** | **str** | The reference number for the item. Please provide the itemSequenceNumber from the &#39;items&#39; segment to refer to that item&#39;s details here. | 
**shipped_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | 
**item_details** | [**ItemDetails**](ItemDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.container_item import ContainerItem

# TODO update the JSON string below
json = "{}"
# create an instance of ContainerItem from a JSON string
container_item_instance = ContainerItem.from_json(json)
# print the JSON string representation of the object
print(ContainerItem.to_json())

# convert the object into a dict
container_item_dict = container_item_instance.to_dict()
# create an instance of ContainerItem from a dict
container_item_from_dict = ContainerItem.from_dict(container_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


