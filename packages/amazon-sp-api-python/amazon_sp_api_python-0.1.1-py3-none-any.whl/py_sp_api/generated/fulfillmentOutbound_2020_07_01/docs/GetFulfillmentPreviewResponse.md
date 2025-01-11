# GetFulfillmentPreviewResponse

The response schema for the `getFulfillmentPreview` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetFulfillmentPreviewResult**](GetFulfillmentPreviewResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.get_fulfillment_preview_response import GetFulfillmentPreviewResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetFulfillmentPreviewResponse from a JSON string
get_fulfillment_preview_response_instance = GetFulfillmentPreviewResponse.from_json(json)
# print the JSON string representation of the object
print(GetFulfillmentPreviewResponse.to_json())

# convert the object into a dict
get_fulfillment_preview_response_dict = get_fulfillment_preview_response_instance.to_dict()
# create an instance of GetFulfillmentPreviewResponse from a dict
get_fulfillment_preview_response_from_dict = GetFulfillmentPreviewResponse.from_dict(get_fulfillment_preview_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


