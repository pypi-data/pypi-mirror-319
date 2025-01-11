# TransportationDetails

Transportation details for this shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ship_mode** | **str** | The type of shipment. | [optional] 
**transportation_mode** | **str** | The mode of transportation for this shipment. | [optional] 
**shipped_date** | **datetime** | Date when shipment is performed by the Vendor to Buyer | [optional] 
**estimated_delivery_date** | **datetime** | Estimated Date on which shipment will be delivered from Vendor to Buyer | [optional] 
**shipment_delivery_date** | **datetime** | Date on which shipment will be delivered from Vendor to Buyer | [optional] 
**carrier_details** | [**CarrierDetails**](CarrierDetails.md) |  | [optional] 
**bill_of_lading_number** | **str** | The Bill of Lading (BOL) number is a unique number assigned to each shipment of goods by the vendor or shipper during the creation of the Bill of Lading. This number must be unique for every shipment and cannot be a date/time or single character. The BOL numer is mandatory in Shipment Confirmation message for FTL and LTL shipments, and must match the paper BOL provided with the shipment. Instead of BOL, an alternative reference number (like Delivery Note Number) for the shipment can also be sent in this field. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.transportation_details import TransportationDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TransportationDetails from a JSON string
transportation_details_instance = TransportationDetails.from_json(json)
# print the JSON string representation of the object
print(TransportationDetails.to_json())

# convert the object into a dict
transportation_details_dict = transportation_details_instance.to_dict()
# create an instance of TransportationDetails from a dict
transportation_details_from_dict = TransportationDetails.from_dict(transportation_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


