# GenerateShipmentContentUpdatePreviewsRequest

The `GenerateShipmentContentUpdatePreviews` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**boxes** | [**List[BoxUpdateInput]**](BoxUpdateInput.md) | A list of boxes that will be present in the shipment after the update. | 
**items** | [**List[ItemInput]**](ItemInput.md) | A list of all items that will be present in the shipment after the update. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.generate_shipment_content_update_previews_request import GenerateShipmentContentUpdatePreviewsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenerateShipmentContentUpdatePreviewsRequest from a JSON string
generate_shipment_content_update_previews_request_instance = GenerateShipmentContentUpdatePreviewsRequest.from_json(json)
# print the JSON string representation of the object
print(GenerateShipmentContentUpdatePreviewsRequest.to_json())

# convert the object into a dict
generate_shipment_content_update_previews_request_dict = generate_shipment_content_update_previews_request_instance.to_dict()
# create an instance of GenerateShipmentContentUpdatePreviewsRequest from a dict
generate_shipment_content_update_previews_request_from_dict = GenerateShipmentContentUpdatePreviewsRequest.from_dict(generate_shipment_content_update_previews_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


