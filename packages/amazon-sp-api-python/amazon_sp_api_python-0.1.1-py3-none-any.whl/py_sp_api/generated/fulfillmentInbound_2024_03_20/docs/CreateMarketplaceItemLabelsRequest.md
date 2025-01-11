# CreateMarketplaceItemLabelsRequest

The `createMarketplaceItemLabels` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**height** | **float** | The height of the item label. | [optional] 
**label_type** | [**LabelPrintType**](LabelPrintType.md) |  | 
**locale_code** | **str** | The locale code constructed from ISO 639 language code and ISO 3166-1 alpha-2 standard of country codes separated by an underscore character. | [optional] [default to 'en_US']
**marketplace_id** | **str** | The Marketplace ID. For a list of possible values, refer to [Marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids). | 
**msku_quantities** | [**List[MskuQuantity]**](MskuQuantity.md) | Represents the quantity of an MSKU to print item labels for. | 
**page_type** | [**ItemLabelPageType**](ItemLabelPageType.md) |  | [optional] 
**width** | **float** | The width of the item label. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.create_marketplace_item_labels_request import CreateMarketplaceItemLabelsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateMarketplaceItemLabelsRequest from a JSON string
create_marketplace_item_labels_request_instance = CreateMarketplaceItemLabelsRequest.from_json(json)
# print the JSON string representation of the object
print(CreateMarketplaceItemLabelsRequest.to_json())

# convert the object into a dict
create_marketplace_item_labels_request_dict = create_marketplace_item_labels_request_instance.to_dict()
# create an instance of CreateMarketplaceItemLabelsRequest from a dict
create_marketplace_item_labels_request_from_dict = CreateMarketplaceItemLabelsRequest.from_dict(create_marketplace_item_labels_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


