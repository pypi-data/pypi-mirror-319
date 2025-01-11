# UnmanifestedCarrierInformation

UnmanifestedCarrierInformation like carrierId CarrierName and Location

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_id** | **str** | The carrier identifier for the offering, provided by the carrier. | [optional] 
**carrier_name** | **str** | The carrier name for the offering. | [optional] 
**unmanifested_shipment_location_list** | [**List[UnmanifestedShipmentLocation]**](UnmanifestedShipmentLocation.md) | A list of UnmanifestedShipmentLocation | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.unmanifested_carrier_information import UnmanifestedCarrierInformation

# TODO update the JSON string below
json = "{}"
# create an instance of UnmanifestedCarrierInformation from a JSON string
unmanifested_carrier_information_instance = UnmanifestedCarrierInformation.from_json(json)
# print the JSON string representation of the object
print(UnmanifestedCarrierInformation.to_json())

# convert the object into a dict
unmanifested_carrier_information_dict = unmanifested_carrier_information_instance.to_dict()
# create an instance of UnmanifestedCarrierInformation from a dict
unmanifested_carrier_information_from_dict = UnmanifestedCarrierInformation.from_dict(unmanifested_carrier_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


