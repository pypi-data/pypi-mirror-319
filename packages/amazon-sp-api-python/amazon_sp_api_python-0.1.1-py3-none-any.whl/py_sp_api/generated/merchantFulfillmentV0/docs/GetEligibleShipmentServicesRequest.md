# GetEligibleShipmentServicesRequest

Request schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipment_request_details** | [**ShipmentRequestDetails**](ShipmentRequestDetails.md) |  | 
**shipping_offering_filter** | [**ShippingOfferingFilter**](ShippingOfferingFilter.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.get_eligible_shipment_services_request import GetEligibleShipmentServicesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetEligibleShipmentServicesRequest from a JSON string
get_eligible_shipment_services_request_instance = GetEligibleShipmentServicesRequest.from_json(json)
# print the JSON string representation of the object
print(GetEligibleShipmentServicesRequest.to_json())

# convert the object into a dict
get_eligible_shipment_services_request_dict = get_eligible_shipment_services_request_instance.to_dict()
# create an instance of GetEligibleShipmentServicesRequest from a dict
get_eligible_shipment_services_request_from_dict = GetEligibleShipmentServicesRequest.from_dict(get_eligible_shipment_services_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


