# Label

Data for creating a shipping label and dimensions for printing the label.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_text_for_label** | **str** | Custom text to print on the label. Note: Custom text is only included on labels that are in ZPL format (ZPL203). FedEx does not support &#x60;CustomTextForLabel&#x60;. | [optional] 
**dimensions** | [**LabelDimensions**](LabelDimensions.md) |  | 
**file_contents** | [**FileContents**](FileContents.md) |  | 
**label_format** | [**LabelFormat**](LabelFormat.md) |  | [optional] 
**standard_id_for_label** | [**StandardIdForLabel**](StandardIdForLabel.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.label import Label

# TODO update the JSON string below
json = "{}"
# create an instance of Label from a JSON string
label_instance = Label.from_json(json)
# print the JSON string representation of the object
print(Label.to_json())

# convert the object into a dict
label_dict = label_instance.to_dict()
# create an instance of Label from a dict
label_from_dict = Label.from_dict(label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


