# GetEligibleShipmentServicesResult

The payload for the `getEligibleShipmentServices` operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**shipping_service_list** | [**List[ShippingService]**](ShippingService.md) | A list of shipping services offers. | 
**rejected_shipping_service_list** | [**List[RejectedShippingService]**](RejectedShippingService.md) | List of services that are for some reason unavailable for this request | [optional] 
**temporarily_unavailable_carrier_list** | [**List[TemporarilyUnavailableCarrier]**](TemporarilyUnavailableCarrier.md) | A list of temporarily unavailable carriers. | [optional] 
**terms_and_conditions_not_accepted_carrier_list** | [**List[TermsAndConditionsNotAcceptedCarrier]**](TermsAndConditionsNotAcceptedCarrier.md) | List of carriers whose terms and conditions were not accepted by the seller. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.get_eligible_shipment_services_result import GetEligibleShipmentServicesResult

# TODO update the JSON string below
json = "{}"
# create an instance of GetEligibleShipmentServicesResult from a JSON string
get_eligible_shipment_services_result_instance = GetEligibleShipmentServicesResult.from_json(json)
# print the JSON string representation of the object
print(GetEligibleShipmentServicesResult.to_json())

# convert the object into a dict
get_eligible_shipment_services_result_dict = get_eligible_shipment_services_result_instance.to_dict()
# create an instance of GetEligibleShipmentServicesResult from a dict
get_eligible_shipment_services_result_from_dict = GetEligibleShipmentServicesResult.from_dict(get_eligible_shipment_services_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


