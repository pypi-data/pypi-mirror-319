# CarrierDetails

Indicates the carrier details and their contact informations

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The field is used to represent the carrier used for performing the shipment. | [optional] 
**code** | **str** | Code that identifies the carrier for the shipment. The Standard Carrier Alpha Code (SCAC) is a unique two to four letter code used to identify a carrier. Carrier SCAC codes are assigned and maintained by the NMFTA (National Motor Freight Association). | [optional] 
**phone** | **str** | The field is used to represent the Carrier contact number. | [optional] 
**email** | **str** | The field is used to represent the carrier Email id. | [optional] 
**shipment_reference_number** | **str** | The field is also known as PRO number is a unique number assigned by the carrier. It is used to identify and track the shipment that goes out for delivery. This field is mandatory for US, CA, MX shipment confirmations. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.carrier_details import CarrierDetails

# TODO update the JSON string below
json = "{}"
# create an instance of CarrierDetails from a JSON string
carrier_details_instance = CarrierDetails.from_json(json)
# print the JSON string representation of the object
print(CarrierDetails.to_json())

# convert the object into a dict
carrier_details_dict = carrier_details_instance.to_dict()
# create an instance of CarrierDetails from a dict
carrier_details_from_dict = CarrierDetails.from_dict(carrier_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


