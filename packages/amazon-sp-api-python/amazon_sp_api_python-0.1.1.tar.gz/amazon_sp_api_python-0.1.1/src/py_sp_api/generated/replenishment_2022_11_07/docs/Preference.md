# Preference

Offer preferences that you can include in the result filter criteria.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auto_enrollment** | [**List[AutoEnrollmentPreference]**](AutoEnrollmentPreference.md) | Filters the results to only include offers with the auto-enrollment preference specified. | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.preference import Preference

# TODO update the JSON string below
json = "{}"
# create an instance of Preference from a JSON string
preference_instance = Preference.from_json(json)
# print the JSON string representation of the object
print(Preference.to_json())

# convert the object into a dict
preference_dict = preference_instance.to_dict()
# create an instance of Preference from a dict
preference_from_dict = Preference.from_dict(preference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


