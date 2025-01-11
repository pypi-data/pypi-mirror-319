# BoxInput

Input information for a given box.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_information_source** | [**BoxContentInformationSource**](BoxContentInformationSource.md) |  | 
**dimensions** | [**Dimensions**](Dimensions.md) |  | 
**items** | [**List[ItemInput]**](ItemInput.md) | The items and their quantity in the box. This must be empty if the box &#x60;contentInformationSource&#x60; is &#x60;BARCODE_2D&#x60; or &#x60;MANUAL_PROCESS&#x60;. | [optional] 
**quantity** | **int** | The number of containers where all other properties like weight or dimensions are identical. | 
**weight** | [**Weight**](Weight.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.box_input import BoxInput

# TODO update the JSON string below
json = "{}"
# create an instance of BoxInput from a JSON string
box_input_instance = BoxInput.from_json(json)
# print the JSON string representation of the object
print(BoxInput.to_json())

# convert the object into a dict
box_input_dict = box_input_instance.to_dict()
# create an instance of BoxInput from a dict
box_input_from_dict = BoxInput.from_dict(box_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


