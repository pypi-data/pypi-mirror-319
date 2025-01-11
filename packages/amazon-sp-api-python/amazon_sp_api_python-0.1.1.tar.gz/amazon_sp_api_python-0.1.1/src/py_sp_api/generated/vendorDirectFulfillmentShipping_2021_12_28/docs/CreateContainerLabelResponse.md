# CreateContainerLabelResponse

The response schema for the `createContainerLabel` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_label** | [**ContainerLabel**](ContainerLabel.md) |  | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.create_container_label_response import CreateContainerLabelResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateContainerLabelResponse from a JSON string
create_container_label_response_instance = CreateContainerLabelResponse.from_json(json)
# print the JSON string representation of the object
print(CreateContainerLabelResponse.to_json())

# convert the object into a dict
create_container_label_response_dict = create_container_label_response_instance.to_dict()
# create an instance of CreateContainerLabelResponse from a dict
create_container_label_response_from_dict = CreateContainerLabelResponse.from_dict(create_container_label_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


