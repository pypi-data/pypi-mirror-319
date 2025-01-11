# LabelCustomization

Custom text for shipping labels.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_text_for_label** | **str** | Custom text to print on the label. Note: Custom text is only included on labels that are in ZPL format (ZPL203). FedEx does not support &#x60;CustomTextForLabel&#x60;. | [optional] 
**standard_id_for_label** | [**StandardIdForLabel**](StandardIdForLabel.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.label_customization import LabelCustomization

# TODO update the JSON string below
json = "{}"
# create an instance of LabelCustomization from a JSON string
label_customization_instance = LabelCustomization.from_json(json)
# print the JSON string representation of the object
print(LabelCustomization.to_json())

# convert the object into a dict
label_customization_dict = label_customization_instance.to_dict()
# create an instance of LabelCustomization from a dict
label_customization_from_dict = LabelCustomization.from_dict(label_customization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


