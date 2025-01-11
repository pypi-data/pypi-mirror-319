# Item

An item in the Amazon catalog.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asin** | **str** | Amazon Standard Identification Number (ASIN) is the unique identifier for an item in the Amazon catalog. | 
**attributes** | **Dict[str, object]** | A JSON object that contains structured item attribute data keyed by attribute name. Catalog item attributes conform to the related product type definitions available in the Selling Partner API for Product Type Definitions. | [optional] 
**classifications** | [**List[ItemBrowseClassificationsByMarketplace]**](ItemBrowseClassificationsByMarketplace.md) | Array of classifications (browse nodes) associated with the item in the Amazon catalog by Amazon marketplace. | [optional] 
**dimensions** | [**List[ItemDimensionsByMarketplace]**](ItemDimensionsByMarketplace.md) | Array of dimensions associated with the item in the Amazon catalog by Amazon marketplace. | [optional] 
**identifiers** | [**List[ItemIdentifiersByMarketplace]**](ItemIdentifiersByMarketplace.md) | Identifiers associated with the item in the Amazon catalog, such as UPC and EAN identifiers. | [optional] 
**images** | [**List[ItemImagesByMarketplace]**](ItemImagesByMarketplace.md) | Images for an item in the Amazon catalog. | [optional] 
**product_types** | [**List[ItemProductTypeByMarketplace]**](ItemProductTypeByMarketplace.md) | Product types associated with the Amazon catalog item. | [optional] 
**relationships** | [**List[ItemRelationshipsByMarketplace]**](ItemRelationshipsByMarketplace.md) | Relationships by marketplace for an Amazon catalog item (for example, variations). | [optional] 
**sales_ranks** | [**List[ItemSalesRanksByMarketplace]**](ItemSalesRanksByMarketplace.md) | Sales ranks of an Amazon catalog item. | [optional] 
**summaries** | [**List[ItemSummaryByMarketplace]**](ItemSummaryByMarketplace.md) | Summary details of an Amazon catalog item. | [optional] 
**vendor_details** | [**List[ItemVendorDetailsByMarketplace]**](ItemVendorDetailsByMarketplace.md) | Vendor details associated with an Amazon catalog item. Vendor details are available to vendors only. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item import Item

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


