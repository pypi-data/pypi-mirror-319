# BusinessHours

Business days and hours when the destination is open for deliveries.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**day_of_week** | **str** | Day of the week. | [optional] 
**open_intervals** | [**List[OpenInterval]**](OpenInterval.md) | Time window during the day when the business is open. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.business_hours import BusinessHours

# TODO update the JSON string below
json = "{}"
# create an instance of BusinessHours from a JSON string
business_hours_instance = BusinessHours.from_json(json)
# print the JSON string representation of the object
print(BusinessHours.to_json())

# convert the object into a dict
business_hours_dict = business_hours_instance.to_dict()
# create an instance of BusinessHours from a dict
business_hours_from_dict = BusinessHours.from_dict(business_hours_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


