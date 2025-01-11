# UnmanifestedShipmentLocation

UnmanifestedShipmentLocation info 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | [**Address**](Address.md) |  | [optional] 
**last_manifest_date** | **str** | Its Last Manifest Date. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.unmanifested_shipment_location import UnmanifestedShipmentLocation

# TODO update the JSON string below
json = "{}"
# create an instance of UnmanifestedShipmentLocation from a JSON string
unmanifested_shipment_location_instance = UnmanifestedShipmentLocation.from_json(json)
# print the JSON string representation of the object
print(UnmanifestedShipmentLocation.to_json())

# convert the object into a dict
unmanifested_shipment_location_dict = unmanifested_shipment_location_instance.to_dict()
# create an instance of UnmanifestedShipmentLocation from a dict
unmanifested_shipment_location_from_dict = UnmanifestedShipmentLocation.from_dict(unmanifested_shipment_location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


