# AvailableDeliveryExperienceOption

The available delivery confirmation options, and the fee charged, if any.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_experience_option** | [**DeliveryExperienceOption**](DeliveryExperienceOption.md) |  | 
**charge** | [**CurrencyAmount**](CurrencyAmount.md) |  | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.available_delivery_experience_option import AvailableDeliveryExperienceOption

# TODO update the JSON string below
json = "{}"
# create an instance of AvailableDeliveryExperienceOption from a JSON string
available_delivery_experience_option_instance = AvailableDeliveryExperienceOption.from_json(json)
# print the JSON string representation of the object
print(AvailableDeliveryExperienceOption.to_json())

# convert the object into a dict
available_delivery_experience_option_dict = available_delivery_experience_option_instance.to_dict()
# create an instance of AvailableDeliveryExperienceOption from a dict
available_delivery_experience_option_from_dict = AvailableDeliveryExperienceOption.from_dict(available_delivery_experience_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


