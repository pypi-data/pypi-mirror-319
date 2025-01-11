# GetFulfillmentPreviewResult

A list of fulfillment order previews, including estimated shipping weights, estimated shipping fees, and estimated ship dates and arrival dates.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fulfillment_previews** | [**List[FulfillmentPreview]**](FulfillmentPreview.md) | An array of fulfillment preview information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_fulfillment_preview_result import GetFulfillmentPreviewResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetFulfillmentPreviewResult from a JSON string
get_fulfillment_preview_result_instance = GetFulfillmentPreviewResult.from_json(json)
# print the JSON string representation of the object
print(GetFulfillmentPreviewResult.to_json())

# convert the object into a dict
get_fulfillment_preview_result_dict = get_fulfillment_preview_result_instance.to_dict()
# create an instance of GetFulfillmentPreviewResult from a dict
get_fulfillment_preview_result_from_dict = GetFulfillmentPreviewResult.from_dict(get_fulfillment_preview_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


