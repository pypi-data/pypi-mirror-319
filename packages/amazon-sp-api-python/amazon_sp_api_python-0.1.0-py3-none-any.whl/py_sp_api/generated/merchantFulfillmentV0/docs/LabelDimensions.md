# LabelDimensions

Dimensions for printing a shipping label.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**length** | **float** | A label dimension. | 
**width** | **float** | A label dimension. | 
**unit** | [**UnitOfLength**](UnitOfLength.md) |  | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.label_dimensions import LabelDimensions

# TODO update the JSON string below
json = "{}"
# create an instance of LabelDimensions from a JSON string
label_dimensions_instance = LabelDimensions.from_json(json)
# print the JSON string representation of the object
print(LabelDimensions.to_json())

# convert the object into a dict
label_dimensions_dict = label_dimensions_instance.to_dict()
# create an instance of LabelDimensions from a dict
label_dimensions_from_dict = LabelDimensions.from_dict(label_dimensions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


