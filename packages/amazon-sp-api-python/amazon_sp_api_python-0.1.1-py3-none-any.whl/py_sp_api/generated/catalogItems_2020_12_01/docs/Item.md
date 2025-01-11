# Item

An item in the Amazon catalog.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | Amazon Standard Identification Number (ASIN) is the unique identifier for an item in the Amazon catalog. | 
**attributes** | **Dict[str, object]** | A JSON object that contains structured item attribute data keyed by attribute name. Catalog item attributes are available only to brand owners and conform to the related product type definitions available in the Selling Partner API for Product Type Definitions. | [optional] 
**identifiers** | [**List[ItemIdentifiersByMarketplace]**](ItemIdentifiersByMarketplace.md) | Identifiers associated with the item in the Amazon catalog, such as UPC and EAN identifiers. | [optional] 
**images** | [**List[ItemImagesByMarketplace]**](ItemImagesByMarketplace.md) | Images for an item in the Amazon catalog. All image variants are provided to brand owners. Otherwise, a thumbnail of the \&quot;MAIN\&quot; image variant is provided. | [optional] 
**product_types** | [**List[ItemProductTypeByMarketplace]**](ItemProductTypeByMarketplace.md) | Product types associated with the Amazon catalog item. | [optional] 
**sales_ranks** | [**List[ItemSalesRanksByMarketplace]**](ItemSalesRanksByMarketplace.md) | Sales ranks of an Amazon catalog item. | [optional] 
**summaries** | [**List[ItemSummaryByMarketplace]**](ItemSummaryByMarketplace.md) | Summary details of an Amazon catalog item. | [optional] 
**variations** | [**List[ItemVariationsByMarketplace]**](ItemVariationsByMarketplace.md) | Variation details by marketplace for an Amazon catalog item (variation relationships). | [optional] 
**vendor_details** | [**List[ItemVendorDetailsByMarketplace]**](ItemVendorDetailsByMarketplace.md) | Vendor details associated with an Amazon catalog item. Vendor details are available to vendors only. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2020_12_01.models.item import Item

# TODO update the JSON string below
json = "{}"
# create an instance of Item from a JSON string
item_instance = Item.from_json(json)
# print the JSON string representation of the object
print(Item.to_json())

# convert the object into a dict
item_dict = item_instance.to_dict()
# create an instance of Item from a dict
item_from_dict = Item.from_dict(item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


