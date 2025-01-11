# DeliveryPreferences

Contains all of the delivery instructions provided by the customer for the shipping address.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**drop_off_location** | **str** | Drop-off location selected by the customer. | [optional] 
**preferred_delivery_time** | [**PreferredDeliveryTime**](PreferredDeliveryTime.md) |  | [optional] 
**other_attributes** | [**List[OtherDeliveryAttributes]**](OtherDeliveryAttributes.md) | Enumerated list of miscellaneous delivery attributes associated with the shipping address. | [optional] 
**address_instructions** | **str** | Building instructions, nearby landmark or navigation instructions. | [optional] 

## Example

```python
from py_sp_api.generated.ordersV0.models.delivery_preferences import DeliveryPreferences

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryPreferences from a JSON string
delivery_preferences_instance = DeliveryPreferences.from_json(json)
# print the JSON string representation of the object
print(DeliveryPreferences.to_json())

# convert the object into a dict
delivery_preferences_dict = delivery_preferences_instance.to_dict()
# create an instance of DeliveryPreferences from a dict
delivery_preferences_from_dict = DeliveryPreferences.from_dict(delivery_preferences_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


