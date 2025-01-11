# ShipmentTransportationConfiguration

Details needed to generate the transportation options.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**contact_information** | [**ContactInformation**](ContactInformation.md) |  | [optional] 
**freight_information** | [**FreightInformation**](FreightInformation.md) |  | [optional] 
**pallets** | [**List[PalletInput]**](PalletInput.md) | List of pallet configuration inputs. | [optional] 
**ready_to_ship_window** | [**WindowInput**](WindowInput.md) |  | 
**shipment_id** | **str** | Identifier of a shipment. A shipment contains the boxes and units being inbounded. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.shipment_transportation_configuration import ShipmentTransportationConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentTransportationConfiguration from a JSON string
shipment_transportation_configuration_instance = ShipmentTransportationConfiguration.from_json(json)
# print the JSON string representation of the object
print(ShipmentTransportationConfiguration.to_json())

# convert the object into a dict
shipment_transportation_configuration_dict = shipment_transportation_configuration_instance.to_dict()
# create an instance of ShipmentTransportationConfiguration from a dict
shipment_transportation_configuration_from_dict = ShipmentTransportationConfiguration.from_dict(shipment_transportation_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


