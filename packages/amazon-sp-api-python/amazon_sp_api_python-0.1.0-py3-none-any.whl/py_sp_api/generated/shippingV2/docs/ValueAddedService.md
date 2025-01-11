# ValueAddedService

A value-added service available for purchase with a shipment service offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The identifier for the value-added service. | 
**name** | **str** | The name of the value-added service. | 
**cost** | [**Currency**](Currency.md) |  | 

## Example

```python
from py_sp_api.generated.shippingV2.models.value_added_service import ValueAddedService

# TODO update the JSON string below
json = "{}"
# create an instance of ValueAddedService from a JSON string
value_added_service_instance = ValueAddedService.from_json(json)
# print the JSON string representation of the object
print(ValueAddedService.to_json())

# convert the object into a dict
value_added_service_dict = value_added_service_instance.to_dict()
# create an instance of ValueAddedService from a dict
value_added_service_from_dict = ValueAddedService.from_dict(value_added_service_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


