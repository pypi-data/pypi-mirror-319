# CreateContainerLabelRequest

The request body schema for the `createContainerLabel` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**ship_from_party** | [**PartyIdentification**](PartyIdentification.md) |  | 
**carrier_id** | [**CarrierId**](CarrierId.md) |  | 
**vendor_container_id** | **str** | The unique, vendor-provided identifier for the container. | 
**packages** | [**List[Package]**](Package.md) | An array of package objects in a container. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.create_container_label_request import CreateContainerLabelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateContainerLabelRequest from a JSON string
create_container_label_request_instance = CreateContainerLabelRequest.from_json(json)
# print the JSON string representation of the object
print(CreateContainerLabelRequest.to_json())

# convert the object into a dict
create_container_label_request_dict = create_container_label_request_instance.to_dict()
# create an instance of CreateContainerLabelRequest from a dict
create_container_label_request_from_dict = CreateContainerLabelRequest.from_dict(create_container_label_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


