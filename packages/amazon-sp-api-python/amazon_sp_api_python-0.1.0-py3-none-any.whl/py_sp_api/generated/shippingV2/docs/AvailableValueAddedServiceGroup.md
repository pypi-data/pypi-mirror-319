# AvailableValueAddedServiceGroup

The value-added services available for purchase with a shipping service offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**group_id** | **str** | The type of the value-added service group. | 
**group_description** | **str** | The name of the value-added service group. | 
**is_required** | **bool** | When true, one or more of the value-added services listed must be specified. | 
**value_added_services** | [**List[ValueAddedService]**](ValueAddedService.md) | A list of optional value-added services available for purchase with a shipping service offering. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.available_value_added_service_group import AvailableValueAddedServiceGroup

# TODO update the JSON string below
json = "{}"
# create an instance of AvailableValueAddedServiceGroup from a JSON string
available_value_added_service_group_instance = AvailableValueAddedServiceGroup.from_json(json)
# print the JSON string representation of the object
print(AvailableValueAddedServiceGroup.to_json())

# convert the object into a dict
available_value_added_service_group_dict = available_value_added_service_group_instance.to_dict()
# create an instance of AvailableValueAddedServiceGroup from a dict
available_value_added_service_group_from_dict = AvailableValueAddedServiceGroup.from_dict(available_value_added_service_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


