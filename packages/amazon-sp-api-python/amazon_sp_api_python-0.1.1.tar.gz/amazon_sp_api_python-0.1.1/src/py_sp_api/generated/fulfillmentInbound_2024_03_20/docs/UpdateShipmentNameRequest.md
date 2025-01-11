# UpdateShipmentNameRequest

The `updateShipmentName` request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | A human-readable name to update the shipment name to. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.update_shipment_name_request import UpdateShipmentNameRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateShipmentNameRequest from a JSON string
update_shipment_name_request_instance = UpdateShipmentNameRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateShipmentNameRequest.to_json())

# convert the object into a dict
update_shipment_name_request_dict = update_shipment_name_request_instance.to_dict()
# create an instance of UpdateShipmentNameRequest from a dict
update_shipment_name_request_from_dict = UpdateShipmentNameRequest.from_dict(update_shipment_name_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


