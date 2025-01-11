# PackageItemDetails

Item details for be provided for every item in shipment at either the item or carton or pallet level, whichever is appropriate.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | The purchase order number for the shipment being confirmed. If the items in this shipment belong to multiple purchase order numbers that are in particular carton or pallet within the shipment, then provide the purchaseOrderNumber at the appropriate carton or pallet level. Formatting Notes: 8-character alpha-numeric code. | [optional] 
**lot_number** | **str** | The batch or lot number associates an item with information the manufacturer considers relevant for traceability of the trade item to which the Element String is applied. The data may refer to the trade item itself or to items contained. This field is mandatory for all perishable items. | [optional] 
**expiry** | [**Expiry**](Expiry.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.package_item_details import PackageItemDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PackageItemDetails from a JSON string
package_item_details_instance = PackageItemDetails.from_json(json)
# print the JSON string representation of the object
print(PackageItemDetails.to_json())

# convert the object into a dict
package_item_details_dict = package_item_details_instance.to_dict()
# create an instance of PackageItemDetails from a dict
package_item_details_from_dict = PackageItemDetails.from_dict(package_item_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


