# OneClickShipmentResponse

The response schema for the OneClickShipment operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**OneClickShipmentResult**](OneClickShipmentResult.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.one_click_shipment_response import OneClickShipmentResponse

# TODO update the JSON string below
json = "{}"
# create an instance of OneClickShipmentResponse from a JSON string
one_click_shipment_response_instance = OneClickShipmentResponse.from_json(json)
# print the JSON string representation of the object
print(OneClickShipmentResponse.to_json())

# convert the object into a dict
one_click_shipment_response_dict = one_click_shipment_response_instance.to_dict()
# create an instance of OneClickShipmentResponse from a dict
one_click_shipment_response_from_dict = OneClickShipmentResponse.from_dict(one_click_shipment_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


