# ContainerLabel

The details of the container label.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_tracking_number** | **str** | The container (pallet) tracking identifier from the shipping carrier. | [optional] 
**content** | **str** | The &#x60;Base64encoded&#x60; string of the container label content. | 
**format** | [**ContainerLabelFormat**](ContainerLabelFormat.md) |  | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.container_label import ContainerLabel

# TODO update the JSON string below
json = "{}"
# create an instance of ContainerLabel from a JSON string
container_label_instance = ContainerLabel.from_json(json)
# print the JSON string representation of the object
print(ContainerLabel.to_json())

# convert the object into a dict
container_label_dict = container_label_instance.to_dict()
# create an instance of ContainerLabel from a dict
container_label_from_dict = ContainerLabel.from_dict(container_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


