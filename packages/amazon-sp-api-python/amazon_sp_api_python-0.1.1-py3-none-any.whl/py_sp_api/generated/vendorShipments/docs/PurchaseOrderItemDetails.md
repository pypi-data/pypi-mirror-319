# PurchaseOrderItemDetails

Item details for be provided for every item in shipment at either the item or carton or pallet level, whichever is appropriate.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**maximum_retail_price** | [**Money**](Money.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.purchase_order_item_details import PurchaseOrderItemDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseOrderItemDetails from a JSON string
purchase_order_item_details_instance = PurchaseOrderItemDetails.from_json(json)
# print the JSON string representation of the object
print(PurchaseOrderItemDetails.to_json())

# convert the object into a dict
purchase_order_item_details_dict = purchase_order_item_details_instance.to_dict()
# create an instance of PurchaseOrderItemDetails from a dict
purchase_order_item_details_from_dict = PurchaseOrderItemDetails.from_dict(purchase_order_item_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


