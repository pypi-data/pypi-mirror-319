# InboundShipmentHeader

Inbound shipment information used to create and update inbound shipments.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_name** | **str** | The name for the shipment. Use a naming convention that helps distinguish between shipments over time, such as the date the shipment was created. | 
**ship_from_address** | [**Address**](Address.md) |  | 
**destination_fulfillment_center_id** | **str** | The identifier for the fulfillment center to which the shipment will be shipped. Get this value from the InboundShipmentPlan object in the response returned by the createInboundShipmentPlan operation. | 
**are_cases_required** | **bool** | Indicates whether or not an inbound shipment contains case-packed boxes. Note: A shipment must contain either all case-packed boxes or all individually packed boxes.  Possible values:  true - All boxes in the shipment must be case packed.  false - All boxes in the shipment must be individually packed.  Note: If AreCasesRequired &#x3D; true for an inbound shipment, then the value of QuantityInCase must be greater than zero for every item in the shipment. Otherwise the service returns an error. | [optional] 
**shipment_status** | [**ShipmentStatus**](ShipmentStatus.md) |  | 
**label_prep_preference** | [**LabelPrepPreference**](LabelPrepPreference.md) |  | 
**intended_box_contents_source** | [**IntendedBoxContentsSource**](IntendedBoxContentsSource.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.inbound_shipment_header import InboundShipmentHeader

# TODO update the JSON string below
json = "{}"
# create an instance of InboundShipmentHeader from a JSON string
inbound_shipment_header_instance = InboundShipmentHeader.from_json(json)
# print the JSON string representation of the object
print(InboundShipmentHeader.to_json())

# convert the object into a dict
inbound_shipment_header_dict = inbound_shipment_header_instance.to_dict()
# create an instance of InboundShipmentHeader from a dict
inbound_shipment_header_from_dict = InboundShipmentHeader.from_dict(inbound_shipment_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


