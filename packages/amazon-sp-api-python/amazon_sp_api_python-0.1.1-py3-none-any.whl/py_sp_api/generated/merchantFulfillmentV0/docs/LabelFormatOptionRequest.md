# LabelFormatOptionRequest

Whether to include a packing slip.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**include_packing_slip_with_label** | **bool** | When true, include a packing slip with the label. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.label_format_option_request import LabelFormatOptionRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LabelFormatOptionRequest from a JSON string
label_format_option_request_instance = LabelFormatOptionRequest.from_json(json)
# print the JSON string representation of the object
print(LabelFormatOptionRequest.to_json())

# convert the object into a dict
label_format_option_request_dict = label_format_option_request_instance.to_dict()
# create an instance of LabelFormatOptionRequest from a dict
label_format_option_request_from_dict = LabelFormatOptionRequest.from_dict(label_format_option_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


