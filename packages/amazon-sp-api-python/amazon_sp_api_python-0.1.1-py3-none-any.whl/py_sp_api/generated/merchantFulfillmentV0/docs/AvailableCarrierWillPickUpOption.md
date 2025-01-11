# AvailableCarrierWillPickUpOption

Indicates whether the carrier will pick up the package, and what fee is charged, if any.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_will_pick_up_option** | [**CarrierWillPickUpOption**](CarrierWillPickUpOption.md) |  | 
**charge** | [**CurrencyAmount**](CurrencyAmount.md) |  | 

## Example

```python
from py_sp_api.generated.merchantFulfillmentV0.models.available_carrier_will_pick_up_option import AvailableCarrierWillPickUpOption

# TODO update the JSON string below
json = "{}"
# create an instance of AvailableCarrierWillPickUpOption from a JSON string
available_carrier_will_pick_up_option_instance = AvailableCarrierWillPickUpOption.from_json(json)
# print the JSON string representation of the object
print(AvailableCarrierWillPickUpOption.to_json())

# convert the object into a dict
available_carrier_will_pick_up_option_dict = available_carrier_will_pick_up_option_instance.to_dict()
# create an instance of AvailableCarrierWillPickUpOption from a dict
available_carrier_will_pick_up_option_from_dict = AvailableCarrierWillPickUpOption.from_dict(available_carrier_will_pick_up_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


