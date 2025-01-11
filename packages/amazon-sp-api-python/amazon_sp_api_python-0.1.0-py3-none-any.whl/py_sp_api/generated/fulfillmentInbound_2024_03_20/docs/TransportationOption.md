# TransportationOption

Contains information pertaining to a transportation option and the related carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier** | [**Carrier**](Carrier.md) |  | 
**carrier_appointment** | [**CarrierAppointment**](CarrierAppointment.md) |  | [optional] 
**preconditions** | **List[str]** | Identifies a list of preconditions for confirming the transportation option. | 
**quote** | [**Quote**](Quote.md) |  | [optional] 
**shipment_id** | **str** | Identifier of a shipment. A shipment contains the boxes and units being inbounded. | 
**shipping_mode** | **str** | Mode of shipment transportation that this option will provide.  Possible values: &#x60;GROUND_SMALL_PARCEL&#x60;, &#x60;FREIGHT_LTL&#x60;, &#x60;FREIGHT_FTL_PALLET&#x60;, &#x60;FREIGHT_FTL_NONPALLET&#x60;, &#x60;OCEAN_LCL&#x60;, &#x60;OCEAN_FCL&#x60;, &#x60;AIR_SMALL_PARCEL&#x60;, &#x60;AIR_SMALL_PARCEL_EXPRESS&#x60;. | 
**shipping_solution** | **str** | Shipping program for the option. Possible values: &#x60;AMAZON_PARTNERED_CARRIER&#x60;, &#x60;USE_YOUR_OWN_CARRIER&#x60;. | 
**transportation_option_id** | **str** | Identifier of a transportation option. A transportation option represent one option for how to send a shipment. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.transportation_option import TransportationOption

# TODO update the JSON string below
json = "{}"
# create an instance of TransportationOption from a JSON string
transportation_option_instance = TransportationOption.from_json(json)
# print the JSON string representation of the object
print(TransportationOption.to_json())

# convert the object into a dict
transportation_option_dict = transportation_option_instance.to_dict()
# create an instance of TransportationOption from a dict
transportation_option_from_dict = TransportationOption.from_dict(transportation_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


