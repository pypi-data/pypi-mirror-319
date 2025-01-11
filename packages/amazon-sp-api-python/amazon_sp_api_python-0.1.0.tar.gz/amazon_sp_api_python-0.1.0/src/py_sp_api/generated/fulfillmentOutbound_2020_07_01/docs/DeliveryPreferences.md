# DeliveryPreferences

The delivery preferences applied to the destination address. These preferences are applied when possible and are best effort. This feature is currently supported only in the JP marketplace and not applicable for other marketplaces. For eligible orders, the default delivery preference will be to deliver the package unattended at the front door, unless you specify otherwise.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_instructions** | **str** | Additional delivery instructions. For example, this could be instructions on how to enter a building, nearby landmark or navigation instructions, &#39;Beware of dogs&#39;, etc. | [optional] 
**drop_off_location** | [**DropOffLocation**](DropOffLocation.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.delivery_preferences import DeliveryPreferences

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


