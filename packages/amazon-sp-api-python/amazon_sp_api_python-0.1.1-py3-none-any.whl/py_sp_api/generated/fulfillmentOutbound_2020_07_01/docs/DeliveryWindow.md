# DeliveryWindow

The time range within which a Scheduled Delivery fulfillment order should be delivered. This is only available in the JP marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_date** | **datetime** | Date timestamp | 
**end_date** | **datetime** | Date timestamp | 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.delivery_window import DeliveryWindow

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryWindow from a JSON string
delivery_window_instance = DeliveryWindow.from_json(json)
# print the JSON string representation of the object
print(DeliveryWindow.to_json())

# convert the object into a dict
delivery_window_dict = delivery_window_instance.to_dict()
# create an instance of DeliveryWindow from a dict
delivery_window_from_dict = DeliveryWindow.from_dict(delivery_window_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


