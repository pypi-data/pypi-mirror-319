# CreateInboundShipmentPlanRequest

The request schema for the createInboundShipmentPlan operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_from_address** | [**Address**](Address.md) |  | 
**label_prep_preference** | [**LabelPrepPreference**](LabelPrepPreference.md) |  | 
**ship_to_country_code** | **str** | The two-character country code for the country where the inbound shipment is to be sent.  Note: Not required. Specifying both ShipToCountryCode and ShipToCountrySubdivisionCode returns an error.   Values:   ShipToCountryCode values for North America:  * CA – Canada  * MX - Mexico  * US - United States  ShipToCountryCode values for MCI sellers in Europe:  * DE – Germany  * ES – Spain  * FR – France  * GB – United Kingdom  * IT – Italy  Default: The country code for the seller&#39;s home marketplace. | [optional] 
**ship_to_country_subdivision_code** | **str** | The two-character country code, followed by a dash and then up to three characters that represent the subdivision of the country where the inbound shipment is to be sent. For example, \&quot;IN-MH\&quot;. In full ISO 3166-2 format.  Note: Not required. Specifying both ShipToCountryCode and ShipToCountrySubdivisionCode returns an error. | [optional] 
**inbound_shipment_plan_request_items** | [**List[InboundShipmentPlanRequestItem]**](InboundShipmentPlanRequestItem.md) | List of inbound shipment plan requests | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.create_inbound_shipment_plan_request import CreateInboundShipmentPlanRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateInboundShipmentPlanRequest from a JSON string
create_inbound_shipment_plan_request_instance = CreateInboundShipmentPlanRequest.from_json(json)
# print the JSON string representation of the object
print(CreateInboundShipmentPlanRequest.to_json())

# convert the object into a dict
create_inbound_shipment_plan_request_dict = create_inbound_shipment_plan_request_instance.to_dict()
# create an instance of CreateInboundShipmentPlanRequest from a dict
create_inbound_shipment_plan_request_from_dict = CreateInboundShipmentPlanRequest.from_dict(create_inbound_shipment_plan_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


