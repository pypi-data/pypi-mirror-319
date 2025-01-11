# UnfulfillableQuantity

The quantity of unfulfillable inventory.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_unfulfillable_quantity** | **int** | The total number of units in Amazon&#39;s fulfillment network in unsellable condition. | [optional] 
**customer_damaged_quantity** | **int** | The number of units in customer damaged disposition. | [optional] 
**warehouse_damaged_quantity** | **int** | The number of units in warehouse damaged disposition. | [optional] 
**distributor_damaged_quantity** | **int** | The number of units in distributor damaged disposition. | [optional] 
**carrier_damaged_quantity** | **int** | The number of units in carrier damaged disposition. | [optional] 
**defective_quantity** | **int** | The number of units in defective disposition. | [optional] 
**expired_quantity** | **int** | The number of units in expired disposition. | [optional] 

## Example

```python
from py_sp_api.generated.fbaInventory.models.unfulfillable_quantity import UnfulfillableQuantity

# TODO update the JSON string below
json = "{}"
# create an instance of UnfulfillableQuantity from a JSON string
unfulfillable_quantity_instance = UnfulfillableQuantity.from_json(json)
# print the JSON string representation of the object
print(UnfulfillableQuantity.to_json())

# convert the object into a dict
unfulfillable_quantity_dict = unfulfillable_quantity_instance.to_dict()
# create an instance of UnfulfillableQuantity from a dict
unfulfillable_quantity_from_dict = UnfulfillableQuantity.from_dict(unfulfillable_quantity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


