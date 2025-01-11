# ContentUpdatePreview

Preview of the changes that will be applied to the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_update_preview_id** | **str** | Identifier of a content update preview. | 
**expiration** | **datetime** | The time at which the content update expires. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mm:ss.sssZ&#x60;. | 
**requested_updates** | [**RequestedUpdates**](RequestedUpdates.md) |  | 
**transportation_option** | [**TransportationOption**](TransportationOption.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.content_update_preview import ContentUpdatePreview

# TODO update the JSON string below
json = "{}"
# create an instance of ContentUpdatePreview from a JSON string
content_update_preview_instance = ContentUpdatePreview.from_json(json)
# print the JSON string representation of the object
print(ContentUpdatePreview.to_json())

# convert the object into a dict
content_update_preview_dict = content_update_preview_instance.to_dict()
# create an instance of ContentUpdatePreview from a dict
content_update_preview_from_dict = ContentUpdatePreview.from_dict(content_update_preview_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


