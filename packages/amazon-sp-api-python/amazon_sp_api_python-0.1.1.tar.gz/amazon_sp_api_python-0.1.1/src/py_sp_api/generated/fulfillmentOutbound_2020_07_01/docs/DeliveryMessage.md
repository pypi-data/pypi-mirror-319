# DeliveryMessage

Localized messaging for a delivery offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**text** | **str** | The message content for a delivery offering. | [optional] 
**locale** | **str** | The locale for the message (for example, en_US). | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.delivery_message import DeliveryMessage

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryMessage from a JSON string
delivery_message_instance = DeliveryMessage.from_json(json)
# print the JSON string representation of the object
print(DeliveryMessage.to_json())

# convert the object into a dict
delivery_message_dict = delivery_message_instance.to_dict()
# create an instance of DeliveryMessage from a dict
delivery_message_from_dict = DeliveryMessage.from_dict(delivery_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


