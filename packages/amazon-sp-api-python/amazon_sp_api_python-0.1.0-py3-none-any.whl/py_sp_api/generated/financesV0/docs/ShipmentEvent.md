# ShipmentEvent

A shipment, refund, guarantee claim, or chargeback.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**amazon_order_id** | **str** | An Amazon-defined identifier for an order. | [optional] 
**seller_order_id** | **str** | A seller-defined identifier for an order. | [optional] 
**marketplace_name** | **str** | The name of the marketplace where the event occurred. | [optional] 
**store_name** | **str** | The name of the store where the event occurred. | [optional] 
**order_charge_list** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charge information on the seller&#39;s account. | [optional] 
**order_charge_adjustment_list** | [**List[ChargeComponent]**](ChargeComponent.md) | A list of charge information on the seller&#39;s account. | [optional] 
**shipment_fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**shipment_fee_adjustment_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**order_fee_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**order_fee_adjustment_list** | [**List[FeeComponent]**](FeeComponent.md) | A list of fee component information. | [optional] 
**direct_payment_list** | [**List[DirectPayment]**](DirectPayment.md) | A list of direct payment information. | [optional] 
**posted_date** | **datetime** | Fields with a schema type of date are in ISO 8601 date time format (for example GroupBeginDate). | [optional] 
**shipment_item_list** | [**List[ShipmentItem]**](ShipmentItem.md) | A list of shipment items. | [optional] 
**shipment_item_adjustment_list** | [**List[ShipmentItem]**](ShipmentItem.md) | A list of shipment items. | [optional] 

## Example

```python
from py_sp_api.generated.financesV0.models.shipment_event import ShipmentEvent

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentEvent from a JSON string
shipment_event_instance = ShipmentEvent.from_json(json)
# print the JSON string representation of the object
print(ShipmentEvent.to_json())

# convert the object into a dict
shipment_event_dict = shipment_event_instance.to_dict()
# create an instance of ShipmentEvent from a dict
shipment_event_from_dict = ShipmentEvent.from_dict(shipment_event_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


