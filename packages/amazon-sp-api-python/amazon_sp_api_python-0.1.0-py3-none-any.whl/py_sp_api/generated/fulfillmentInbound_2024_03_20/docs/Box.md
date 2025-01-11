# Box

Contains information about a box that is used in the inbound plan. The box is a container that holds multiple items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**box_id** | **str** | The ID provided by Amazon that identifies a given box. This ID is comprised of the external shipment ID (which is generated after transportation has been confirmed) and the index of the box. | [optional] 
**content_information_source** | [**BoxContentInformationSource**](BoxContentInformationSource.md) |  | [optional] 
**destination_region** | [**Region**](Region.md) |  | [optional] 
**dimensions** | [**Dimensions**](Dimensions.md) |  | [optional] 
**items** | [**List[Item]**](Item.md) | Items contained within the box. | [optional] 
**package_id** | **str** | Primary key to uniquely identify a Package (Box or Pallet). | 
**quantity** | **int** | The number of containers where all other properties like weight or dimensions are identical. | [optional] 
**template_name** | **str** | Template name of the box. | [optional] 
**weight** | [**Weight**](Weight.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.box import Box

# TODO update the JSON string below
json = "{}"
# create an instance of Box from a JSON string
box_instance = Box.from_json(json)
# print the JSON string representation of the object
print(Box.to_json())

# convert the object into a dict
box_dict = box_instance.to_dict()
# create an instance of Box from a dict
box_from_dict = Box.from_dict(box_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


