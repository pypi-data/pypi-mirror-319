# GenerateShipmentContentUpdatePreviewsResponse

The `GenerateShipmentContentUpdatePreviews` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_shipment_content_update_previews_response import GenerateShipmentContentUpdatePreviewsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateShipmentContentUpdatePreviewsResponse from a JSON string
generate_shipment_content_update_previews_response_instance = GenerateShipmentContentUpdatePreviewsResponse.from_json(json)
# print the JSON string representation of the object
print(GenerateShipmentContentUpdatePreviewsResponse.to_json())

# convert the object into a dict
generate_shipment_content_update_previews_response_dict = generate_shipment_content_update_previews_response_instance.to_dict()
# create an instance of GenerateShipmentContentUpdatePreviewsResponse from a dict
generate_shipment_content_update_previews_response_from_dict = GenerateShipmentContentUpdatePreviewsResponse.from_dict(generate_shipment_content_update_previews_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


