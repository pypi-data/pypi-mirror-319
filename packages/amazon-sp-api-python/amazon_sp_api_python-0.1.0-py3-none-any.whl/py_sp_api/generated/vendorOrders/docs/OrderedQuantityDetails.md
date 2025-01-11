# OrderedQuantityDetails

Details of item quantity ordered.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**updated_date** | **datetime** | The date when the line item quantity was updated by buyer. Must be in ISO-8601 date/time format. | [optional] 
**ordered_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 
**cancelled_quantity** | [**ItemQuantity**](ItemQuantity.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorOrders.models.ordered_quantity_details import OrderedQuantityDetails

# TODO update the JSON string below
json = "{}"
# create an instance of OrderedQuantityDetails from a JSON string
ordered_quantity_details_instance = OrderedQuantityDetails.from_json(json)
# print the JSON string representation of the object
print(OrderedQuantityDetails.to_json())

# convert the object into a dict
ordered_quantity_details_dict = ordered_quantity_details_instance.to_dict()
# create an instance of OrderedQuantityDetails from a dict
ordered_quantity_details_from_dict = OrderedQuantityDetails.from_dict(ordered_quantity_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


