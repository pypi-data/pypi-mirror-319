# LabelResult

Label details including label stream, format, size.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**container_reference_id** | **str** | An identifier for the container. This must be unique within all the containers in the same shipment. | [optional] 
**tracking_id** | **str** | The tracking identifier assigned to the container. | [optional] 
**label** | [**Label**](Label.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.label_result import LabelResult

# TODO update the JSON string below
json = "{}"
# create an instance of LabelResult from a JSON string
label_result_instance = LabelResult.from_json(json)
# print the JSON string representation of the object
print(LabelResult.to_json())

# convert the object into a dict
label_result_dict = label_result_instance.to_dict()
# create an instance of LabelResult from a dict
label_result_from_dict = LabelResult.from_dict(label_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


