# OneClickShipmentValueAddedService

A value-added service to be applied to a shipping service purchase.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The identifier of the selected value-added service. | 
**amount** | [**Currency**](Currency.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.one_click_shipment_value_added_service import OneClickShipmentValueAddedService

# TODO update the JSON string below
json = "{}"
# create an instance of OneClickShipmentValueAddedService from a JSON string
one_click_shipment_value_added_service_instance = OneClickShipmentValueAddedService.from_json(json)
# print the JSON string representation of the object
print(OneClickShipmentValueAddedService.to_json())

# convert the object into a dict
one_click_shipment_value_added_service_dict = one_click_shipment_value_added_service_instance.to_dict()
# create an instance of OneClickShipmentValueAddedService from a dict
one_click_shipment_value_added_service_from_dict = OneClickShipmentValueAddedService.from_dict(one_click_shipment_value_added_service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


