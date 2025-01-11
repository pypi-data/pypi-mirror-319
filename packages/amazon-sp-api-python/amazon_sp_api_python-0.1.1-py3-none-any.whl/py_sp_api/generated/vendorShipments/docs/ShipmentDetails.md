# ShipmentDetails

The request schema for the GetShipmentDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**shipments** | [**List[Shipment]**](Shipment.md) | A list of one or more shipments with underlying details. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.shipment_details import ShipmentDetails

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


