# ShippingServiceOptions

Extra services provided by a carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_experience** | [**DeliveryExperienceType**](DeliveryExperienceType.md) |  | 
**declared_value** | [**CurrencyAmount**](CurrencyAmount.md) |  | [optional] 
**carrier_will_pick_up** | **bool** | When true, the carrier will pick up the package. Note: Scheduled carrier pickup is available only using Dynamex (US), DPD (UK), and Royal Mail (UK). | 
**carrier_will_pick_up_option** | [**CarrierWillPickUpOption**](CarrierWillPickUpOption.md) |  | [optional] 
**label_format** | [**LabelFormat**](LabelFormat.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.shipping_service_options import ShippingServiceOptions

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingServiceOptions from a JSON string
shipping_service_options_instance = ShippingServiceOptions.from_json(json)
# print the JSON string representation of the object
print(ShippingServiceOptions.to_json())

# convert the object into a dict
shipping_service_options_dict = shipping_service_options_instance.to_dict()
# create an instance of ShippingServiceOptions from a dict
shipping_service_options_from_dict = ShippingServiceOptions.from_dict(shipping_service_options_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


