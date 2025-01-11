# ListShipmentContentUpdatePreviewsResponse

The `ListShipmentContentUpdatePreviews` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_update_previews** | [**List[ContentUpdatePreview]**](ContentUpdatePreview.md) | A list of content update previews in a shipment. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_shipment_content_update_previews_response import ListShipmentContentUpdatePreviewsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListShipmentContentUpdatePreviewsResponse from a JSON string
list_shipment_content_update_previews_response_instance = ListShipmentContentUpdatePreviewsResponse.from_json(json)
# print the JSON string representation of the object
print(ListShipmentContentUpdatePreviewsResponse.to_json())

# convert the object into a dict
list_shipment_content_update_previews_response_dict = list_shipment_content_update_previews_response_instance.to_dict()
# create an instance of ListShipmentContentUpdatePreviewsResponse from a dict
list_shipment_content_update_previews_response_from_dict = ListShipmentContentUpdatePreviewsResponse.from_dict(list_shipment_content_update_previews_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


