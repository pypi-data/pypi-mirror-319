# Label

The label details of the container.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_stream** | **str** | Contains binary image data encoded as a base-64 string. | [optional] 
**label_specification** | [**LabelSpecification**](LabelSpecification.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.label import Label

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


