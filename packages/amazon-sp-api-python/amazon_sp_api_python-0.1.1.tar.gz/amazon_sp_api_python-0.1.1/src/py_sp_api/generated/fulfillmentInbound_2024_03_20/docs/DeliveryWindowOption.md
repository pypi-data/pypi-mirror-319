# DeliveryWindowOption

Contains information pertaining to a delivery window option.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**availability_type** | **str** | Identifies type of Delivery Window Availability. Values: &#x60;AVAILABLE&#x60;, &#x60;CONGESTED&#x60; | 
**delivery_window_option_id** | **str** | Identifier of a delivery window option. A delivery window option represent one option for when a shipment is expected to be delivered. | 
**end_date** | **datetime** | The time at which this delivery window option ends. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mmZ&#x60;. | 
**start_date** | **datetime** | The time at which this delivery window option starts. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mmZ&#x60;. | 
**valid_until** | **datetime** | The time at which this window delivery option is no longer valid. In [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) datetime format with pattern &#x60;yyyy-MM-ddTHH:mmZ&#x60;. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.delivery_window_option import DeliveryWindowOption

# TODO update the JSON string below
json = "{}"
# create an instance of DeliveryWindowOption from a JSON string
delivery_window_option_instance = DeliveryWindowOption.from_json(json)
# print the JSON string representation of the object
print(DeliveryWindowOption.to_json())

# convert the object into a dict
delivery_window_option_dict = delivery_window_option_instance.to_dict()
# create an instance of DeliveryWindowOption from a dict
delivery_window_option_from_dict = DeliveryWindowOption.from_dict(delivery_window_option_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


