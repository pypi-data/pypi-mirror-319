# GetEligibleShipmentServicesResponse

Response schema.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetEligibleShipmentServicesResult**](GetEligibleShipmentServicesResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.get_eligible_shipment_services_response import GetEligibleShipmentServicesResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetEligibleShipmentServicesResponse from a JSON string
get_eligible_shipment_services_response_instance = GetEligibleShipmentServicesResponse.from_json(json)
# print the JSON string representation of the object
print(GetEligibleShipmentServicesResponse.to_json())

# convert the object into a dict
get_eligible_shipment_services_response_dict = get_eligible_shipment_services_response_instance.to_dict()
# create an instance of GetEligibleShipmentServicesResponse from a dict
get_eligible_shipment_services_response_from_dict = GetEligibleShipmentServicesResponse.from_dict(get_eligible_shipment_services_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


