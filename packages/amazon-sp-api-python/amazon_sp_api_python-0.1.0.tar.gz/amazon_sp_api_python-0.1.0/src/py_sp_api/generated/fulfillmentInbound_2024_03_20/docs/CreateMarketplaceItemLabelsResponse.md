# CreateMarketplaceItemLabelsResponse

The `createMarketplaceItemLabels` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**document_downloads** | [**List[DocumentDownload]**](DocumentDownload.md) | Resources to download the requested document. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.create_marketplace_item_labels_response import CreateMarketplaceItemLabelsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateMarketplaceItemLabelsResponse from a JSON string
create_marketplace_item_labels_response_instance = CreateMarketplaceItemLabelsResponse.from_json(json)
# print the JSON string representation of the object
print(CreateMarketplaceItemLabelsResponse.to_json())

# convert the object into a dict
create_marketplace_item_labels_response_dict = create_marketplace_item_labels_response_instance.to_dict()
# create an instance of CreateMarketplaceItemLabelsResponse from a dict
create_marketplace_item_labels_response_from_dict = CreateMarketplaceItemLabelsResponse.from_dict(create_marketplace_item_labels_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


