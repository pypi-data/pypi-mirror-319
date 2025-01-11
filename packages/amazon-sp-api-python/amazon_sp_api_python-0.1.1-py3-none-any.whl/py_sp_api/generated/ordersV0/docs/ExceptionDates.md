# ExceptionDates

Dates when the business is closed or open with a different time window.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exception_date** | **str** | Date when the business is closed, in &lt;a href&#x3D;&#39;https://developer-docs.amazon.com/sp-api/docs/iso-8601&#39;&gt;ISO 8601&lt;/a&gt; date format. | [optional] 
**is_open** | **bool** | Boolean indicating if the business is closed or open on that date. | [optional] 
**open_intervals** | [**List[OpenInterval]**](OpenInterval.md) | Time window during the day when the business is open. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.exception_dates import ExceptionDates

# TODO update the JSON string below
json = "{}"
# create an instance of ExceptionDates from a JSON string
exception_dates_instance = ExceptionDates.from_json(json)
# print the JSON string representation of the object
print(ExceptionDates.to_json())

# convert the object into a dict
exception_dates_dict = exception_dates_instance.to_dict()
# create an instance of ExceptionDates from a dict
exception_dates_from_dict = ExceptionDates.from_dict(exception_dates_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


