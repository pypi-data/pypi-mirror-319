# RemovalShipmentItemAdjustment

Item-level information for a removal shipment item adjustment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**removal_shipment_item_id** | **str** | An identifier for an item in a removal shipment. | [optional] 
**tax_collection_model** | **str** | The tax collection model applied to the item.  Possible values:  * MarketplaceFacilitator - Tax is withheld and remitted to the taxing authority by Amazon on behalf of the seller.  * Standard - Tax is paid to the seller and not remitted to the taxing authority by Amazon. | [optional] 
**fulfillment_network_sku** | **str** | The Amazon fulfillment network SKU for the item. | [optional] 
**adjusted_quantity** | **int** | Adjusted quantity of removal shipmentItemAdjustment items. | [optional] 
**revenue_adjustment** | [**Currency**](Currency.md) |  | [optional] 
**tax_amount_adjustment** | [**Currency**](Currency.md) |  | [optional] 
**tax_withheld_adjustment** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.removal_shipment_item_adjustment import RemovalShipmentItemAdjustment

# TODO update the JSON string below
json = "{}"
# create an instance of RemovalShipmentItemAdjustment from a JSON string
removal_shipment_item_adjustment_instance = RemovalShipmentItemAdjustment.from_json(json)
# print the JSON string representation of the object
print(RemovalShipmentItemAdjustment.to_json())

# convert the object into a dict
removal_shipment_item_adjustment_dict = removal_shipment_item_adjustment_instance.to_dict()
# create an instance of RemovalShipmentItemAdjustment from a dict
removal_shipment_item_adjustment_from_dict = RemovalShipmentItemAdjustment.from_dict(removal_shipment_item_adjustment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


