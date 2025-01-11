# OneClickShipmentRequest

The request schema for the OneClickShipment operation. When the channelType is not Amazon, shipTo is required and when channelType is Amazon shipTo is ignored.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_to** | [**Address**](Address.md) |  | [optional] 
**ship_from** | [**Address**](Address.md) |  | 
**return_to** | [**Address**](Address.md) |  | [optional] 
**ship_date** | **datetime** | The ship date and time (the requested pickup). This defaults to the current date and time. | [optional] 
**packages** | [**List[Package]**](Package.md) | A list of packages to be shipped through a shipping service offering. | 
**value_added_services_details** | [**List[OneClickShipmentValueAddedService]**](OneClickShipmentValueAddedService.md) | The value-added services to be added to a shipping service purchase. | [optional] 
**tax_details** | [**List[TaxDetail]**](TaxDetail.md) | A list of tax detail information. | [optional] 
**channel_details** | [**ChannelDetails**](ChannelDetails.md) |  | 
**label_specifications** | [**RequestedDocumentSpecification**](RequestedDocumentSpecification.md) |  | 
**service_selection** | [**ServiceSelection**](ServiceSelection.md) |  | 
**shipper_instruction** | [**ShipperInstruction**](ShipperInstruction.md) |  | [optional] 
**destination_access_point_details** | [**AccessPointDetails**](AccessPointDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.one_click_shipment_request import OneClickShipmentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of OneClickShipmentRequest from a JSON string
one_click_shipment_request_instance = OneClickShipmentRequest.from_json(json)
# print the JSON string representation of the object
print(OneClickShipmentRequest.to_json())

# convert the object into a dict
one_click_shipment_request_dict = one_click_shipment_request_instance.to_dict()
# create an instance of OneClickShipmentRequest from a dict
one_click_shipment_request_from_dict = OneClickShipmentRequest.from_dict(one_click_shipment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


