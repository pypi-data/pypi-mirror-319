# ShipmentDetails

Shipment details required for the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_priority_shipment** | **bool** | When true, this is a priority shipment. | 
**is_scheduled_delivery_shipment** | **bool** | When true, this order is part of a scheduled delivery program. | [optional] 
**is_pslip_required** | **bool** | When true, a packing slip is required to be sent to the customer. | 
**is_gift** | **bool** | When true, the order contain a gift. Include the gift message and gift wrap information. | [optional] 
**ship_method** | **str** | Ship method to be used for shipping the order. Amazon defines ship method codes indicating the shipping carrier and shipment service level. To see the full list of ship methods in use, including both the code and the friendly name, search the &#39;Help&#39; section on Vendor Central for &#39;ship methods&#39;. | 
**shipment_dates** | [**ShipmentDates**](ShipmentDates.md) |  | 
**message_to_customer** | **str** | Message to customer for order status. | 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.shipment_details import ShipmentDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentDetails from a JSON string
shipment_details_instance = ShipmentDetails.from_json(json)
# print the JSON string representation of the object
print(ShipmentDetails.to_json())

# convert the object into a dict
shipment_details_dict = shipment_details_instance.to_dict()
# create an instance of ShipmentDetails from a dict
shipment_details_from_dict = ShipmentDetails.from_dict(shipment_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


