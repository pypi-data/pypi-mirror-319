# SubstitutionPreferences

Substitution preferences for an order item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**substitution_type** | **str** | The type of substitution that these preferences represent. | 
**substitution_options** | [**List[SubstitutionOption]**](SubstitutionOption.md) | A collection of substitution options. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.substitution_preferences import SubstitutionPreferences

# TODO update the JSON string below
json = "{}"
# create an instance of SubstitutionPreferences from a JSON string
substitution_preferences_instance = SubstitutionPreferences.from_json(json)
# print the JSON string representation of the object
print(SubstitutionPreferences.to_json())

# convert the object into a dict
substitution_preferences_dict = substitution_preferences_instance.to_dict()
# create an instance of SubstitutionPreferences from a dict
substitution_preferences_from_dict = SubstitutionPreferences.from_dict(substitution_preferences_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


