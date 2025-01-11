# LabelFormatOption

The label format details and whether to include a packing slip.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**include_packing_slip_with_label** | **bool** | When true, include a packing slip with the label. | [optional] 
**label_format** | [**LabelFormat**](LabelFormat.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.label_format_option import LabelFormatOption

# TODO update the JSON string below
json = "{}"
# create an instance of LabelFormatOption from a JSON string
label_format_option_instance = LabelFormatOption.from_json(json)
# print the JSON string representation of the object
print(LabelFormatOption.to_json())

# convert the object into a dict
label_format_option_dict = label_format_option_instance.to_dict()
# create an instance of LabelFormatOption from a dict
label_format_option_from_dict = LabelFormatOption.from_dict(label_format_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


