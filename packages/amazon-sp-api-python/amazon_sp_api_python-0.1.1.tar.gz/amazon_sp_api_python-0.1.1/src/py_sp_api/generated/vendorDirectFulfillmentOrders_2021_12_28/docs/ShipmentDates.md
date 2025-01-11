# ShipmentDates

Shipment dates.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**required_ship_date** | **datetime** | Time by which the vendor is required to ship the order. | 
**promised_delivery_date** | **datetime** | Delivery date promised to the Amazon customer. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrders_2021_12_28.models.shipment_dates import ShipmentDates

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentDates from a JSON string
shipment_dates_instance = ShipmentDates.from_json(json)
# print the JSON string representation of the object
print(ShipmentDates.to_json())

# convert the object into a dict
shipment_dates_dict = shipment_dates_instance.to_dict()
# create an instance of ShipmentDates from a dict
shipment_dates_from_dict = ShipmentDates.from_dict(shipment_dates_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


