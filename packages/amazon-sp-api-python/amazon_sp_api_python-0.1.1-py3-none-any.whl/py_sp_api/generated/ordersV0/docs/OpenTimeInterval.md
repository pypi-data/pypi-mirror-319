# OpenTimeInterval

The time when the business opens or closes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hour** | **int** | The hour when the business opens or closes. | [optional] 
**minute** | **int** | The minute when the business opens or closes. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.open_time_interval import OpenTimeInterval

# TODO update the JSON string below
json = "{}"
# create an instance of OpenTimeInterval from a JSON string
open_time_interval_instance = OpenTimeInterval.from_json(json)
# print the JSON string representation of the object
print(OpenTimeInterval.to_json())

# convert the object into a dict
open_time_interval_dict = open_time_interval_instance.to_dict()
# create an instance of OpenTimeInterval from a dict
open_time_interval_from_dict = OpenTimeInterval.from_dict(open_time_interval_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


