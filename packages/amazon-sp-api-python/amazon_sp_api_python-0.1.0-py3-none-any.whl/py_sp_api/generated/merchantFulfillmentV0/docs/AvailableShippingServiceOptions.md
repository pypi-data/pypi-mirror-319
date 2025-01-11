# AvailableShippingServiceOptions

The available shipping service options.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**available_carrier_will_pick_up_options** | [**List[AvailableCarrierWillPickUpOption]**](AvailableCarrierWillPickUpOption.md) | List of available carrier pickup options. | 
**available_delivery_experience_options** | [**List[AvailableDeliveryExperienceOption]**](AvailableDeliveryExperienceOption.md) | List of available delivery experience options. | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.available_shipping_service_options import AvailableShippingServiceOptions

# TODO update the JSON string below
json = "{}"
# create an instance of AvailableShippingServiceOptions from a JSON string
available_shipping_service_options_instance = AvailableShippingServiceOptions.from_json(json)
# print the JSON string representation of the object
print(AvailableShippingServiceOptions.to_json())

# convert the object into a dict
available_shipping_service_options_dict = available_shipping_service_options_instance.to_dict()
# create an instance of AvailableShippingServiceOptions from a dict
available_shipping_service_options_from_dict = AvailableShippingServiceOptions.from_dict(available_shipping_service_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


