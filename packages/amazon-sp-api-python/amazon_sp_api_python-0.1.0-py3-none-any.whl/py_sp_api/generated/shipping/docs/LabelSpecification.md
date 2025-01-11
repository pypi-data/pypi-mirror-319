# LabelSpecification

The label specification info.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_format** | **str** | The format of the label. Enum of PNG only for now. | 
**label_stock_size** | **str** | The label stock size specification in length and height. Enum of 4x6 only for now. | 

## Example

```python
from py_sp_api.generated.shipping.models.label_specification import LabelSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of LabelSpecification from a JSON string
label_specification_instance = LabelSpecification.from_json(json)
# print the JSON string representation of the object
print(LabelSpecification.to_json())

# convert the object into a dict
label_specification_dict = label_specification_instance.to_dict()
# create an instance of LabelSpecification from a dict
label_specification_from_dict = LabelSpecification.from_dict(label_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


