# ListingsItemPatchRequest

The request body schema for the `patchListingsItem` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_type** | **str** | The Amazon product type of the listings item. | 
**patches** | [**List[PatchOperation]**](PatchOperation.md) | One or more JSON Patch operations to perform on the listings item. | 

## Example

```python
from py_sp_api.generated.listingsItems_2021_08_01.models.listings_item_patch_request import ListingsItemPatchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListingsItemPatchRequest from a JSON string
listings_item_patch_request_instance = ListingsItemPatchRequest.from_json(json)
# print the JSON string representation of the object
print(ListingsItemPatchRequest.to_json())

# convert the object into a dict
listings_item_patch_request_dict = listings_item_patch_request_instance.to_dict()
# create an instance of ListingsItemPatchRequest from a dict
listings_item_patch_request_from_dict = ListingsItemPatchRequest.from_dict(listings_item_patch_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


