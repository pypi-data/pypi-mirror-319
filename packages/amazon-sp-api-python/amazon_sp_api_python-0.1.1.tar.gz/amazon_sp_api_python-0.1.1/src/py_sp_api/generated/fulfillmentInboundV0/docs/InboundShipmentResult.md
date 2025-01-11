# InboundShipmentResult

Result of an inbound shipment operation

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_id** | **str** | The shipment identifier submitted in the request. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_result import InboundShipmentResult

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentResult from a JSON string
inbound_shipment_result_instance = InboundShipmentResult.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentResult.to_json())

# convert the object into a dict
inbound_shipment_result_dict = inbound_shipment_result_instance.to_dict()
# create an instance of InboundShipmentResult from a dict
inbound_shipment_result_from_dict = InboundShipmentResult.from_dict(inbound_shipment_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


