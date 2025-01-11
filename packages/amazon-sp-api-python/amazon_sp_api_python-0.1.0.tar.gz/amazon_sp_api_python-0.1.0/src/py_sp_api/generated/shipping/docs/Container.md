# Container

Container in the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_type** | **str** | The type of physical container being used. (always &#39;PACKAGE&#39;) | [optional] 
**container_reference_id** | **str** | An identifier for the container. This must be unique within all the containers in the same shipment. | 
**value** | [**Currency**](Currency.md) |  | 
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**items** | [**List[ContainerItem]**](ContainerItem.md) | A list of the items in the container. | 
**weight** | [**Weight**](Weight.md) |  | 

## Example

```python
from py_sp_api.generated.shipping.models.container import Container

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


