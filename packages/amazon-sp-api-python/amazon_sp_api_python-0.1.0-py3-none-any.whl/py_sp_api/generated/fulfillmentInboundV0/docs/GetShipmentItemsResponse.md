# GetShipmentItemsResponse

The response schema for the getShipmentItems operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**GetShipmentItemsResult**](GetShipmentItemsResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.get_shipment_items_response import GetShipmentItemsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GetShipmentItemsResponse from a JSON string
get_shipment_items_response_instance = GetShipmentItemsResponse.from_json(json)
# print the JSON string representation of the object
print(GetShipmentItemsResponse.to_json())

# convert the object into a dict
get_shipment_items_response_dict = get_shipment_items_response_instance.to_dict()
# create an instance of GetShipmentItemsResponse from a dict
get_shipment_items_response_from_dict = GetShipmentItemsResponse.from_dict(get_shipment_items_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


