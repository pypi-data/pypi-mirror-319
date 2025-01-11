# OfferProgramConfigurationPreferences

An object which contains the preferences applied to the offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auto_enrollment** | [**AutoEnrollmentPreference**](AutoEnrollmentPreference.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.offer_program_configuration_preferences import OfferProgramConfigurationPreferences

# TODO update the JSON string below
json = "{}"
# create an instance of OfferProgramConfigurationPreferences from a JSON string
offer_program_configuration_preferences_instance = OfferProgramConfigurationPreferences.from_json(json)
# print the JSON string representation of the object
print(OfferProgramConfigurationPreferences.to_json())

# convert the object into a dict
offer_program_configuration_preferences_dict = offer_program_configuration_preferences_instance.to_dict()
# create an instance of OfferProgramConfigurationPreferences from a dict
offer_program_configuration_preferences_from_dict = OfferProgramConfigurationPreferences.from_dict(offer_program_configuration_preferences_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


