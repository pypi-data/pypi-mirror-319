# ShipmentStatusDetails

Shipment Status details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_status** | **str** | Current status of the shipment on whether it is picked up or scheduled. | [optional] 
**shipment_status_date** | **datetime** | Date and time on last status update received for the shipment | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.shipment_status_details import ShipmentStatusDetails

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentStatusDetails from a JSON string
shipment_status_details_instance = ShipmentStatusDetails.from_json(json)
# print the JSON string representation of the object
print(ShipmentStatusDetails.to_json())

# convert the object into a dict
shipment_status_details_dict = shipment_status_details_instance.to_dict()
# create an instance of ShipmentStatusDetails from a dict
shipment_status_details_from_dict = ShipmentStatusDetails.from_dict(shipment_status_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


