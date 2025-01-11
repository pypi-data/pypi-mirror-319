# ContainerIdentification

A list of carton identifiers.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_identification_type** | **str** | The container identification type. | 
**container_identification_number** | **str** | Container identification number that adheres to the definition of the container identification type. | 

## Example

```python
from py_sp_api.generated.vendorShipments.models.container_identification import ContainerIdentification

# TODO update the JSON string below
json = "{}"
# create an instance of ContainerIdentification from a JSON string
container_identification_instance = ContainerIdentification.from_json(json)
# print the JSON string representation of the object
print(ContainerIdentification.to_json())

# convert the object into a dict
container_identification_dict = container_identification_instance.to_dict()
# create an instance of ContainerIdentification from a dict
container_identification_from_dict = ContainerIdentification.from_dict(container_identification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


