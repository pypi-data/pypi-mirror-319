# RemovalShipmentItem

Item-level information for a removal shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**removal_shipment_item_id** | **str** | An identifier for an item in a removal shipment. | [optional] 
**tax_collection_model** | **str** | The tax collection model applied to the item.  Possible values:  * MarketplaceFacilitator - Tax is withheld and remitted to the taxing authority by Amazon on behalf of the seller.  * Standard - Tax is paid to the seller and not remitted to the taxing authority by Amazon. | [optional] 
**fulfillment_network_sku** | **str** | The Amazon fulfillment network SKU for the item. | [optional] 
**quantity** | **int** | The quantity of the item. | [optional] 
**revenue** | [**Currency**](Currency.md) |  | [optional] 
**fee_amount** | [**Currency**](Currency.md) |  | [optional] 
**tax_amount** | [**Currency**](Currency.md) |  | [optional] 
**tax_withheld** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.removal_shipment_item import RemovalShipmentItem

# TODO update the JSON string below
json = "{}"
# create an instance of RemovalShipmentItem from a JSON string
removal_shipment_item_instance = RemovalShipmentItem.from_json(json)
# print the JSON string representation of the object
print(RemovalShipmentItem.to_json())

# convert the object into a dict
removal_shipment_item_dict = removal_shipment_item_instance.to_dict()
# create an instance of RemovalShipmentItem from a dict
removal_shipment_item_from_dict = RemovalShipmentItem.from_dict(removal_shipment_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


