# OfferProgramConfiguration

The offer program configuration contains a set of program properties for an offer.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**preferences** | [**OfferProgramConfigurationPreferences**](OfferProgramConfigurationPreferences.md) |  | [optional] 
**promotions** | [**OfferProgramConfigurationPromotions**](OfferProgramConfigurationPromotions.md) |  | [optional] 
**enrollment_method** | [**EnrollmentMethod**](EnrollmentMethod.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.replenishment_2022_11_07.models.offer_program_configuration import OfferProgramConfiguration

# TODO update the JSON string below
json = "{}"
# create an instance of OfferProgramConfiguration from a JSON string
offer_program_configuration_instance = OfferProgramConfiguration.from_json(json)
# print the JSON string representation of the object
print(OfferProgramConfiguration.to_json())

# convert the object into a dict
offer_program_configuration_dict = offer_program_configuration_instance.to_dict()
# create an instance of OfferProgramConfiguration from a dict
offer_program_configuration_from_dict = OfferProgramConfiguration.from_dict(offer_program_configuration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


