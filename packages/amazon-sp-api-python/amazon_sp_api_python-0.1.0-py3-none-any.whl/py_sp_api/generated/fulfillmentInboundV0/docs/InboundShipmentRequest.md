# InboundShipmentRequest

The request schema for an inbound shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_shipment_header** | [**InboundShipmentHeader**](InboundShipmentHeader.md) |  | 
**inbound_shipment_items** | [**List[InboundShipmentItem]**](InboundShipmentItem.md) | A list of inbound shipment item information. | 
**marketplace_id** | **str** | A marketplace identifier. Specifies the marketplace where the product would be stored. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_request import InboundShipmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentRequest from a JSON string
inbound_shipment_request_instance = InboundShipmentRequest.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentRequest.to_json())

# convert the object into a dict
inbound_shipment_request_dict = inbound_shipment_request_instance.to_dict()
# create an instance of InboundShipmentRequest from a dict
inbound_shipment_request_from_dict = InboundShipmentRequest.from_dict(inbound_shipment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


