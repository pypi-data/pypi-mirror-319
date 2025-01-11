# OpenInterval

The time interval for which the business is open.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_time** | [**OpenTimeInterval**](OpenTimeInterval.md) |  | [optional] 
**end_time** | [**OpenTimeInterval**](OpenTimeInterval.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.open_interval import OpenInterval

# TODO update the JSON string below
json = "{}"
# create an instance of OpenInterval from a JSON string
open_interval_instance = OpenInterval.from_json(json)
# print the JSON string representation of the object
print(OpenInterval.to_json())

# convert the object into a dict
open_interval_dict = open_interval_instance.to_dict()
# create an instance of OpenInterval from a dict
open_interval_from_dict = OpenInterval.from_dict(open_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


