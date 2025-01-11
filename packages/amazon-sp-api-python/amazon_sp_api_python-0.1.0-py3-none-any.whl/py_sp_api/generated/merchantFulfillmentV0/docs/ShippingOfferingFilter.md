# ShippingOfferingFilter

Filter for use when requesting eligible shipping services.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**include_packing_slip_with_label** | **bool** | When true, include a packing slip with the label. | [optional] 
**include_complex_shipping_options** | **bool** | When true, include complex shipping options. | [optional] 
**carrier_will_pick_up** | [**CarrierWillPickUpOption**](CarrierWillPickUpOption.md) |  | [optional] 
**delivery_experience** | [**DeliveryExperienceOption**](DeliveryExperienceOption.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.shipping_offering_filter import ShippingOfferingFilter

# TODO update the JSON string below
json = "{}"
# create an instance of ShippingOfferingFilter from a JSON string
shipping_offering_filter_instance = ShippingOfferingFilter.from_json(json)
# print the JSON string representation of the object
print(ShippingOfferingFilter.to_json())

# convert the object into a dict
shipping_offering_filter_dict = shipping_offering_filter_instance.to_dict()
# create an instance of ShippingOfferingFilter from a dict
shipping_offering_filter_from_dict = ShippingOfferingFilter.from_dict(shipping_offering_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


