# RetrieveShippingLabelResult

The payload schema for the retrieveShippingLabel operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label_stream** | **str** | Contains binary image data encoded as a base-64 string. | 
**label_specification** | [**LabelSpecification**](LabelSpecification.md) |  | 

## Example

```python
from py_sp_api.generated.shipping.models.retrieve_shipping_label_result import RetrieveShippingLabelResult

# TODO update the JSON string below
json = "{}"
# create an instance of RetrieveShippingLabelResult from a JSON string
retrieve_shipping_label_result_instance = RetrieveShippingLabelResult.from_json(json)
# print the JSON string representation of the object
print(RetrieveShippingLabelResult.to_json())

# convert the object into a dict
retrieve_shipping_label_result_dict = retrieve_shipping_label_result_instance.to_dict()
# create an instance of RetrieveShippingLabelResult from a dict
retrieve_shipping_label_result_from_dict = RetrieveShippingLabelResult.from_dict(retrieve_shipping_label_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


