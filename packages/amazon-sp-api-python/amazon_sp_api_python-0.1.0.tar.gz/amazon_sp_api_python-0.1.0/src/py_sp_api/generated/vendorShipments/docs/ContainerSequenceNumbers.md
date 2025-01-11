# ContainerSequenceNumbers

Container sequence numbers that are involved in this shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_sequence_number** | **str** | A list of containers shipped | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.container_sequence_numbers import ContainerSequenceNumbers

# TODO update the JSON string below
json = "{}"
# create an instance of ContainerSequenceNumbers from a JSON string
container_sequence_numbers_instance = ContainerSequenceNumbers.from_json(json)
# print the JSON string representation of the object
print(ContainerSequenceNumbers.to_json())

# convert the object into a dict
container_sequence_numbers_dict = container_sequence_numbers_instance.to_dict()
# create an instance of ContainerSequenceNumbers from a dict
container_sequence_numbers_from_dict = ContainerSequenceNumbers.from_dict(container_sequence_numbers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


