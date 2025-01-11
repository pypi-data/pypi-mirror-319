# ItemVendorDetailsCategory

Product category or subcategory associated with an Amazon catalog item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_name** | **str** | Display name of the product category or subcategory | [optional] 
**value** | **str** | Value (code) of the product category or subcategory. | [optional] 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.item_vendor_details_category import ItemVendorDetailsCategory

# TODO update the JSON string below
json = "{}"
# create an instance of ItemVendorDetailsCategory from a JSON string
item_vendor_details_category_instance = ItemVendorDetailsCategory.from_json(json)
# print the JSON string representation of the object
print(ItemVendorDetailsCategory.to_json())

# convert the object into a dict
item_vendor_details_category_dict = item_vendor_details_category_instance.to_dict()
# create an instance of ItemVendorDetailsCategory from a dict
item_vendor_details_category_from_dict = ItemVendorDetailsCategory.from_dict(item_vendor_details_category_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


