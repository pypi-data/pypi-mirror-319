# GetShipmentResponse

The response schema for the getShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**Shipment**](Shipment.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.get_shipment_response import GetShipmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentResponse from a JSON string
get_shipment_response_instance = GetShipmentResponse.from_json(json)
# print the JSON string representation of the object
print(GetShipmentResponse.to_json())

# convert the object into a dict
get_shipment_response_dict = get_shipment_response_instance.to_dict()
# create an instance of GetShipmentResponse from a dict
get_shipment_response_from_dict = GetShipmentResponse.from_dict(get_shipment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


