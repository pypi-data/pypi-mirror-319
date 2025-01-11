# TransportShipmentMeasurements

Shipment measurement details.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_carton_count** | **int** | Total number of cartons present in the shipment. Provide the cartonCount only for non-palletized shipments. | [optional] 
**total_pallet_stackable** | **int** | Total number of Stackable Pallets present in the shipment. | [optional] 
**total_pallet_non_stackable** | **int** | Total number of Non Stackable Pallets present in the shipment. | [optional] 
**shipment_weight** | [**Weight**](Weight.md) |  | [optional] 
**shipment_volume** | [**Volume**](Volume.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.transport_shipment_measurements import TransportShipmentMeasurements

# TODO update the JSON string below
json = "{}"
# create an instance of TransportShipmentMeasurements from a JSON string
transport_shipment_measurements_instance = TransportShipmentMeasurements.from_json(json)
# print the JSON string representation of the object
print(TransportShipmentMeasurements.to_json())

# convert the object into a dict
transport_shipment_measurements_dict = transport_shipment_measurements_instance.to_dict()
# create an instance of TransportShipmentMeasurements from a dict
transport_shipment_measurements_from_dict = TransportShipmentMeasurements.from_dict(transport_shipment_measurements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


