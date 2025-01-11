# CreateShipmentResponse

The response schema for the createShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CreateShipmentResult**](CreateShipmentResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.create_shipment_response import CreateShipmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of CreateShipmentResponse from a JSON string
create_shipment_response_instance = CreateShipmentResponse.from_json(json)
# print the JSON string representation of the object
print(CreateShipmentResponse.to_json())

# convert the object into a dict
create_shipment_response_dict = create_shipment_response_instance.to_dict()
# create an instance of CreateShipmentResponse from a dict
create_shipment_response_from_dict = CreateShipmentResponse.from_dict(create_shipment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


