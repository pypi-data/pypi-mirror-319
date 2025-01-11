# UpdateShipmentSourceAddressRequest

The `UpdateShipmentSourceAddress` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**address** | [**AddressInput**](AddressInput.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_shipment_source_address_request import UpdateShipmentSourceAddressRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateShipmentSourceAddressRequest from a JSON string
update_shipment_source_address_request_instance = UpdateShipmentSourceAddressRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateShipmentSourceAddressRequest.to_json())

# convert the object into a dict
update_shipment_source_address_request_dict = update_shipment_source_address_request_instance.to_dict()
# create an instance of UpdateShipmentSourceAddressRequest from a dict
update_shipment_source_address_request_from_dict = UpdateShipmentSourceAddressRequest.from_dict(update_shipment_source_address_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


