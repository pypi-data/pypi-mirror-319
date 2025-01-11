# TransportHeader

The shipping identifier, information about whether the shipment is by an Amazon-partnered carrier, and information about whether the shipment is Small Parcel or Less Than Truckload/Full Truckload (LTL/FTL).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_id** | **str** | The Amazon seller identifier. | 
**shipment_id** | **str** | A shipment identifier originally returned by the createInboundShipmentPlan operation. | 
**is_partnered** | **bool** | Indicates whether a putTransportDetails request is for a partnered carrier.  Possible values:  * true – Request is for an Amazon-partnered carrier.  * false – Request is for a non-Amazon-partnered carrier. | 
**shipment_type** | [**ShipmentType**](ShipmentType.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.transport_header import TransportHeader

# TODO update the JSON string below
json = "{}"
# create an instance of TransportHeader from a JSON string
transport_header_instance = TransportHeader.from_json(json)
# print the JSON string representation of the object
print(TransportHeader.to_json())

# convert the object into a dict
transport_header_dict = transport_header_instance.to_dict()
# create an instance of TransportHeader from a dict
transport_header_from_dict = TransportHeader.from_dict(transport_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


