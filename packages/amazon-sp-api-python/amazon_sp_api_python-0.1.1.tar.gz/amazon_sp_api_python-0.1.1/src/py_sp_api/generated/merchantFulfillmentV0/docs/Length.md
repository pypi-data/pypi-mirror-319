# Length

The length.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **float** | The value in units. | [optional] 
**unit** | [**UnitOfLength**](UnitOfLength.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.length import Length

# TODO update the JSON string below
json = "{}"
# create an instance of Length from a JSON string
length_instance = Length.from_json(json)
# print the JSON string representation of the object
print(Length.to_json())

# convert the object into a dict
length_dict = length_instance.to_dict()
# create an instance of Length from a dict
length_from_dict = Length.from_dict(length_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


