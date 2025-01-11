# Duration

The duration of time.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **int** | An unsigned integer that can be only positive or zero. | [optional] 
**time_unit** | [**TimeUnit**](TimeUnit.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.supplySources_2020_07_01.models.duration import Duration

# TODO update the JSON string below
json = "{}"
# create an instance of Duration from a JSON string
duration_instance = Duration.from_json(json)
# print the JSON string representation of the object
print(Duration.to_json())

# convert the object into a dict
duration_dict = duration_instance.to_dict()
# create an instance of Duration from a dict
duration_from_dict = Duration.from_dict(duration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


