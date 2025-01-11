# UpdateShipmentSourceAddressResponse

The `UpdateShipmentSourceAddress` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation_id** | **str** | UUID for the given operation. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_shipment_source_address_response import UpdateShipmentSourceAddressResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateShipmentSourceAddressResponse from a JSON string
update_shipment_source_address_response_instance = UpdateShipmentSourceAddressResponse.from_json(json)
# print the JSON string representation of the object
print(UpdateShipmentSourceAddressResponse.to_json())

# convert the object into a dict
update_shipment_source_address_response_dict = update_shipment_source_address_response_instance.to_dict()
# create an instance of UpdateShipmentSourceAddressResponse from a dict
update_shipment_source_address_response_from_dict = UpdateShipmentSourceAddressResponse.from_dict(update_shipment_source_address_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


