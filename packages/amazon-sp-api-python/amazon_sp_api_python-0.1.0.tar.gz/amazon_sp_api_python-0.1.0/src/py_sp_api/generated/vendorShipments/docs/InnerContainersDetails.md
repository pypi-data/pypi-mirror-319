# InnerContainersDetails

Details of the innerContainersDetails.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_count** | **int** | Total containers as part of the shipment | [optional] 
**container_sequence_numbers** | [**List[ContainerSequenceNumbers]**](ContainerSequenceNumbers.md) | Container sequence numbers that are involved in this shipment. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.inner_containers_details import InnerContainersDetails

# TODO update the JSON string below
json = "{}"
# create an instance of InnerContainersDetails from a JSON string
inner_containers_details_instance = InnerContainersDetails.from_json(json)
# print the JSON string representation of the object
print(InnerContainersDetails.to_json())

# convert the object into a dict
inner_containers_details_dict = inner_containers_details_instance.to_dict()
# create an instance of InnerContainersDetails from a dict
inner_containers_details_from_dict = InnerContainersDetails.from_dict(inner_containers_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


