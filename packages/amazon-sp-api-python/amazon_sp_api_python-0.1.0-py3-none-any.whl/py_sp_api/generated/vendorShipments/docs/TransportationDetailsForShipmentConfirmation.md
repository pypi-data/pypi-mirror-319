# TransportationDetailsForShipmentConfirmation

Transportation details for this shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_scac** | **str** | Code that identifies the carrier for the shipment. The Standard Carrier Alpha Code (SCAC) is a unique two to four letter code used to identify a carrier. Carrier SCAC codes are assigned and maintained by the NMFTA (National Motor Freight Association). This field is mandatory for US, CA, MX shipment confirmations. | [optional] 
**carrier_shipment_reference_number** | **str** | The field also known as PRO number is a unique number assigned by the carrier. It is used to identify and track the shipment that goes out for delivery. This field is mandatory for UA, CA, MX shipment confirmations. | [optional] 
**transportation_mode** | **str** | The mode of transportation for this shipment. | [optional] 
**bill_of_lading_number** | **str** | The Bill of Lading (BOL) number is a unique number assigned to each shipment of goods by the vendor or shipper during the creation of the Bill of Lading. This number must be unique for every shipment and cannot be a date/time or single character. The BOL numer is mandatory in Shipment Confirmation message for FTL and LTL shipments, and must match the paper BOL provided with the shipment. Instead of BOL, an alternative reference number (like Delivery Note Number) for the shipment can also be sent in this field. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.transportation_details_for_shipment_confirmation import TransportationDetailsForShipmentConfirmation

# TODO update the JSON string below
json = "{}"
# create an instance of TransportationDetailsForShipmentConfirmation from a JSON string
transportation_details_for_shipment_confirmation_instance = TransportationDetailsForShipmentConfirmation.from_json(json)
# print the JSON string representation of the object
print(TransportationDetailsForShipmentConfirmation.to_json())

# convert the object into a dict
transportation_details_for_shipment_confirmation_dict = transportation_details_for_shipment_confirmation_instance.to_dict()
# create an instance of TransportationDetailsForShipmentConfirmation from a dict
transportation_details_for_shipment_confirmation_from_dict = TransportationDetailsForShipmentConfirmation.from_dict(transportation_details_for_shipment_confirmation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


