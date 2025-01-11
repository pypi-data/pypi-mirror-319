# GetItemEligibilityPreviewResponse

The response schema for the getItemEligibilityPreview operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ItemEligibilityPreview**](ItemEligibilityPreview.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInbound.models.get_item_eligibility_preview_response import GetItemEligibilityPreviewResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetItemEligibilityPreviewResponse from a JSON string
get_item_eligibility_preview_response_instance = GetItemEligibilityPreviewResponse.from_json(json)
# print the JSON string representation of the object
print(GetItemEligibilityPreviewResponse.to_json())

# convert the object into a dict
get_item_eligibility_preview_response_dict = get_item_eligibility_preview_response_instance.to_dict()
# create an instance of GetItemEligibilityPreviewResponse from a dict
get_item_eligibility_preview_response_from_dict = GetItemEligibilityPreviewResponse.from_dict(get_item_eligibility_preview_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


