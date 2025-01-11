# PurchaseOrders

Transport Request pickup date

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**purchase_order_number** | **str** | Purchase order numbers involved in this shipment, list all the PO that are involved as part of this shipment. | [optional] 
**purchase_order_date** | **datetime** | Purchase order numbers involved in this shipment, list all the PO that are involved as part of this shipment. | [optional] 
**ship_window** | **str** | Date range in which shipment is expected for these purchase orders. | [optional] 
**items** | [**List[PurchaseOrderItems]**](PurchaseOrderItems.md) | A list of the items that are associated to the PO in this transport and their associated details. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.purchase_orders import PurchaseOrders

# TODO update the JSON string below
json = "{}"
# create an instance of PurchaseOrders from a JSON string
purchase_orders_instance = PurchaseOrders.from_json(json)
# print the JSON string representation of the object
print(PurchaseOrders.to_json())

# convert the object into a dict
purchase_orders_dict = purchase_orders_instance.to_dict()
# create an instance of PurchaseOrders from a dict
purchase_orders_from_dict = PurchaseOrders.from_dict(purchase_orders_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


