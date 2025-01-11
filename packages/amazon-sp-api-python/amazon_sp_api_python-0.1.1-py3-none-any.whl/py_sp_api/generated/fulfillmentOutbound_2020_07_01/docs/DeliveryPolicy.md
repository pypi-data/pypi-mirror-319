# DeliveryPolicy

The policy for a delivery offering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | [**DeliveryMessage**](DeliveryMessage.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.delivery_policy import DeliveryPolicy

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryPolicy from a JSON string
delivery_policy_instance = DeliveryPolicy.from_json(json)
# print the JSON string representation of the object
print(DeliveryPolicy.to_json())

# convert the object into a dict
delivery_policy_dict = delivery_policy_instance.to_dict()
# create an instance of DeliveryPolicy from a dict
delivery_policy_from_dict = DeliveryPolicy.from_dict(delivery_policy_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


