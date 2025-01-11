# ContainerItem

Item in the container.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**quantity** | **float** | The quantity of the items of this type in the container. | 
**unit_price** | [**Currency**](Currency.md) |  | 
**unit_weight** | [**Weight**](Weight.md) |  | 
**title** | **str** | A descriptive title of the item. | 

## Example

```python
from py_sp_api.generated.shipping.models.container_item import ContainerItem

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


