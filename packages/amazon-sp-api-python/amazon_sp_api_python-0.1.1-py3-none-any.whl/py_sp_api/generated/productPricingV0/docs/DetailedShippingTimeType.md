# DetailedShippingTimeType

The time range in which an item will likely be shipped once an order has been placed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**minimum_hours** | **int** | The minimum time, in hours, that the item will likely be shipped after the order has been placed. | [optional] 
**maximum_hours** | **int** | The maximum time, in hours, that the item will likely be shipped after the order has been placed. | [optional] 
**available_date** | **str** | The date when the item will be available for shipping. Only displayed for items that are not currently available for shipping. | [optional] 
**availability_type** | **str** | Indicates whether the item is available for shipping now, or on a known or an unknown date in the future. If known, the availableDate property indicates the date that the item will be available for shipping. Possible values: NOW, FUTURE_WITHOUT_DATE, FUTURE_WITH_DATE. | [optional] 

## Example

```python
from py_sp_api.generated.productPricingV0.models.detailed_shipping_time_type import DetailedShippingTimeType

# TODO update the JSON string below
json = "{}"
# create an instance of DetailedShippingTimeType from a JSON string
detailed_shipping_time_type_instance = DetailedShippingTimeType.from_json(json)
# print the JSON string representation of the object
print(DetailedShippingTimeType.to_json())

# convert the object into a dict
detailed_shipping_time_type_dict = detailed_shipping_time_type_instance.to_dict()
# create an instance of DetailedShippingTimeType from a dict
detailed_shipping_time_type_from_dict = DetailedShippingTimeType.from_dict(detailed_shipping_time_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


