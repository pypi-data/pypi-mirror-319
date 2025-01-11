# ContainerSpecification

Container specification for checking the service rate.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**weight** | [**Weight**](Weight.md) |  | 

## Example

```python
from py_sp_api.generated.shipping.models.container_specification import ContainerSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of ContainerSpecification from a JSON string
container_specification_instance = ContainerSpecification.from_json(json)
# print the JSON string representation of the object
print(ContainerSpecification.to_json())

# convert the object into a dict
container_specification_dict = container_specification_instance.to_dict()
# create an instance of ContainerSpecification from a dict
container_specification_from_dict = ContainerSpecification.from_dict(container_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


