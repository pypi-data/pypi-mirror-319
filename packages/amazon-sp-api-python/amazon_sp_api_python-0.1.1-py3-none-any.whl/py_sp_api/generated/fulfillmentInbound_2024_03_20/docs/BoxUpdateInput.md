# BoxUpdateInput

Input information for updating a box

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_information_source** | [**BoxContentInformationSource**](BoxContentInformationSource.md) |  | 
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**items** | [**List[ItemInput]**](ItemInput.md) | The items and their quantity in the box. This must be empty if the box &#x60;contentInformationSource&#x60; is &#x60;BARCODE_2D&#x60; or &#x60;MANUAL_PROCESS&#x60;. | [optional] 
**package_id** | **str** | Primary key to uniquely identify a Box Package. PackageId must be provided if the intent is to update an existing box. Adding a new box will not require providing this value. Any existing PackageIds not provided will be treated as to-be-removed | [optional] 
**quantity** | **int** | The number of containers where all other properties like weight or dimensions are identical. | 
**weight** | [**Weight**](Weight.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.box_update_input import BoxUpdateInput

# TODO update the JSON string below
json = "{}"
# create an instance of BoxUpdateInput from a JSON string
box_update_input_instance = BoxUpdateInput.from_json(json)
# print the JSON string representation of the object
print(BoxUpdateInput.to_json())

# convert the object into a dict
box_update_input_dict = box_update_input_instance.to_dict()
# create an instance of BoxUpdateInput from a dict
box_update_input_from_dict = BoxUpdateInput.from_dict(box_update_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


