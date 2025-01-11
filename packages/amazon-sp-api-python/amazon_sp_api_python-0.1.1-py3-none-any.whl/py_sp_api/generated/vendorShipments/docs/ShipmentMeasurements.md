# ShipmentMeasurements

Shipment measurement details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gross_shipment_weight** | [**Weight**](Weight.md) |  | [optional] 
**shipment_volume** | [**Volume**](Volume.md) |  | [optional] 
**carton_count** | **int** | Number of cartons present in the shipment. Provide the cartonCount only for non-palletized shipments. | [optional] 
**pallet_count** | **int** | Number of pallets present in the shipment. Provide the palletCount only for palletized shipments. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.shipment_measurements import ShipmentMeasurements

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentMeasurements from a JSON string
shipment_measurements_instance = ShipmentMeasurements.from_json(json)
# print the JSON string representation of the object
print(ShipmentMeasurements.to_json())

# convert the object into a dict
shipment_measurements_dict = shipment_measurements_instance.to_dict()
# create an instance of ShipmentMeasurements from a dict
shipment_measurements_from_dict = ShipmentMeasurements.from_dict(shipment_measurements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


