# ItemVendorDetailsByMarketplace

Vendor details associated with an Amazon catalog item for the indicated Amazon marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**marketplace_id** | **str** | Amazon marketplace identifier. | 
**brand_code** | **str** | Brand code associated with an Amazon catalog item. | [optional] 
**manufacturer_code** | **str** | Manufacturer code associated with an Amazon catalog item. | [optional] 
**manufacturer_code_parent** | **str** | Parent vendor code of the manufacturer code. | [optional] 
**product_category** | [**ItemVendorDetailsCategory**](ItemVendorDetailsCategory.md) |  | [optional] 
**product_group** | **str** | Product group associated with an Amazon catalog item. | [optional] 
**product_subcategory** | [**ItemVendorDetailsCategory**](ItemVendorDetailsCategory.md) |  | [optional] 
**replenishment_category** | **str** | Replenishment category associated with an Amazon catalog item. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_vendor_details_by_marketplace import ItemVendorDetailsByMarketplace

# TODO update the JSON string below
json = "{}"
# create an instance of ItemVendorDetailsByMarketplace from a JSON string
item_vendor_details_by_marketplace_instance = ItemVendorDetailsByMarketplace.from_json(json)
# print the JSON string representation of the object
print(ItemVendorDetailsByMarketplace.to_json())

# convert the object into a dict
item_vendor_details_by_marketplace_dict = item_vendor_details_by_marketplace_instance.to_dict()
# create an instance of ItemVendorDetailsByMarketplace from a dict
item_vendor_details_by_marketplace_from_dict = ItemVendorDetailsByMarketplace.from_dict(item_vendor_details_by_marketplace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


