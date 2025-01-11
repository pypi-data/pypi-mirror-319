# PreferredDeliveryTime

The time window when the delivery is preferred.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**business_hours** | [**List[BusinessHours]**](BusinessHours.md) | Business hours when the business is open for deliveries. | [optional] 
**exception_dates** | [**List[ExceptionDates]**](ExceptionDates.md) | Dates when the business is closed during the next 30 days. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.preferred_delivery_time import PreferredDeliveryTime

# TODO update the JSON string below
json = "{}"
# create an instance of PreferredDeliveryTime from a JSON string
preferred_delivery_time_instance = PreferredDeliveryTime.from_json(json)
# print the JSON string representation of the object
print(PreferredDeliveryTime.to_json())

# convert the object into a dict
preferred_delivery_time_dict = preferred_delivery_time_instance.to_dict()
# create an instance of PreferredDeliveryTime from a dict
preferred_delivery_time_from_dict = PreferredDeliveryTime.from_dict(preferred_delivery_time_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


