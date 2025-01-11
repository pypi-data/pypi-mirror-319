# VendorDetails

Vendor Details as part of Label response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**selling_party** | [**PartyIdentification**](PartyIdentification.md) |  | [optional] 
**vendor_shipment_identifier** | **str** | Unique vendor shipment id which is not used in last 365 days | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.vendor_details import VendorDetails

# TODO update the JSON string below
json = "{}"
# create an instance of VendorDetails from a JSON string
vendor_details_instance = VendorDetails.from_json(json)
# print the JSON string representation of the object
print(VendorDetails.to_json())

# convert the object into a dict
vendor_details_dict = vendor_details_instance.to_dict()
# create an instance of VendorDetails from a dict
vendor_details_from_dict = VendorDetails.from_dict(vendor_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


