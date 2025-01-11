# PutTransportDetailsRequest

The request schema for a putTransportDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_partnered** | **bool** | Indicates whether a putTransportDetails request is for an Amazon-partnered carrier. | 
**shipment_type** | [**ShipmentType**](ShipmentType.md) |  | 
**transport_details** | [**TransportDetailInput**](TransportDetailInput.md) |  | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.put_transport_details_request import PutTransportDetailsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PutTransportDetailsRequest from a JSON string
put_transport_details_request_instance = PutTransportDetailsRequest.from_json(json)
# print the JSON string representation of the object
print(PutTransportDetailsRequest.to_json())

# convert the object into a dict
put_transport_details_request_dict = put_transport_details_request_instance.to_dict()
# create an instance of PutTransportDetailsRequest from a dict
put_transport_details_request_from_dict = PutTransportDetailsRequest.from_dict(put_transport_details_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


