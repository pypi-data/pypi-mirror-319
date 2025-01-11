# ConfirmShipmentContentUpdatePreviewResponse

The `confirmShipmentContentUpdatePreview` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.confirm_shipment_content_update_preview_response import ConfirmShipmentContentUpdatePreviewResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ConfirmShipmentContentUpdatePreviewResponse from a JSON string
confirm_shipment_content_update_preview_response_instance = ConfirmShipmentContentUpdatePreviewResponse.from_json(json)
# print the JSON string representation of the object
print(ConfirmShipmentContentUpdatePreviewResponse.to_json())

# convert the object into a dict
confirm_shipment_content_update_preview_response_dict = confirm_shipment_content_update_preview_response_instance.to_dict()
# create an instance of ConfirmShipmentContentUpdatePreviewResponse from a dict
confirm_shipment_content_update_preview_response_from_dict = ConfirmShipmentContentUpdatePreviewResponse.from_dict(confirm_shipment_content_update_preview_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


