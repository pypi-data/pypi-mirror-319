# GetShipmentsResponse

The response schema for the getShipments operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetShipmentsResult**](GetShipmentsResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_shipments_response import GetShipmentsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentsResponse from a JSON string
get_shipments_response_instance = GetShipmentsResponse.from_json(json)
# print the JSON string representation of the object
print(GetShipmentsResponse.to_json())

# convert the object into a dict
get_shipments_response_dict = get_shipments_response_instance.to_dict()
# create an instance of GetShipmentsResponse from a dict
get_shipments_response_from_dict = GetShipmentsResponse.from_dict(get_shipments_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


