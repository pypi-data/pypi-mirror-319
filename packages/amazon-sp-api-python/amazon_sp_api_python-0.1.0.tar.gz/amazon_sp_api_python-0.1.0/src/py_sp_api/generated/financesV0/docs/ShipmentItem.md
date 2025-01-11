# ShipmentItem

An item of a shipment, refund, guarantee claim, or chargeback.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_sku** | **str** | The seller SKU of the item. The seller SKU is qualified by the seller&#39;s seller ID, which is included with every call to the Selling Partner API. | [optional] 
**order_item_id** | **str** | An Amazon-defined order item identifier. | [optional] 
**order_adjustment_item_id** | **str** | An Amazon-defined order adjustment identifier defined for refunds, guarantee claims, and chargeback events. | [optional] 
**quantity_shipped** | **int** | The number of items shipped. | [optional] 
**item_charge_list** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charge information on the seller&#39;s account. | [optional] 
**item_charge_adjustment_list** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charge information on the seller&#39;s account. | [optional] 
**item_fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**item_fee_adjustment_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**item_tax_withheld_list** | [**List[TaxWithheldComponent]**](TaxWithheldComponent.md) | A list of information about taxes withheld. | [optional] 
**promotion_list** | [**List[Promotion]**](Promotion.md) | A list of promotions. | [optional] 
**promotion_adjustment_list** | [**List[Promotion]**](Promotion.md) | A list of promotions. | [optional] 
**cost_of_points_granted** | [**Currency**](Currency.md) |  | [optional] 
**cost_of_points_returned** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.shipment_item import ShipmentItem

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentItem from a JSON string
shipment_item_instance = ShipmentItem.from_json(json)
# print the JSON string representation of the object
print(ShipmentItem.to_json())

# convert the object into a dict
shipment_item_dict = shipment_item_instance.to_dict()
# create an instance of ShipmentItem from a dict
shipment_item_from_dict = ShipmentItem.from_dict(shipment_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


