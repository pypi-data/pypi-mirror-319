# InventoryDetails

Additional inventory details. This object is only displayed if the details parameter in the request is set to `SHOW`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**available_distributable_quantity** | **int** | Quantity that is available for downstream channel replenishment. | [optional] 
**reserved_distributable_quantity** | **int** | Quantity that is reserved for a downstream channel replenishment order that is being prepared for shipment. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.inventory_details import InventoryDetails

# TODO update the JSON string below
json = "{}"
# create an instance of InventoryDetails from a JSON string
inventory_details_instance = InventoryDetails.from_json(json)
# print the JSON string representation of the object
print(InventoryDetails.to_json())

# convert the object into a dict
inventory_details_dict = inventory_details_instance.to_dict()
# create an instance of InventoryDetails from a dict
inventory_details_from_dict = InventoryDetails.from_dict(inventory_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


