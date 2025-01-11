# GetShipmentDetailsResponse

The response schema for the getShipmentDetails operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**ShipmentDetail**](ShipmentDetail.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipmentInvoicingV0.models.get_shipment_details_response import GetShipmentDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentDetailsResponse from a JSON string
get_shipment_details_response_instance = GetShipmentDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(GetShipmentDetailsResponse.to_json())

# convert the object into a dict
get_shipment_details_response_dict = get_shipment_details_response_instance.to_dict()
# create an instance of GetShipmentDetailsResponse from a dict
get_shipment_details_response_from_dict = GetShipmentDetailsResponse.from_dict(get_shipment_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


