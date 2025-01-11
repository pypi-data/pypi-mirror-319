# SelectedDeliveryWindow

Selected delivery window attributes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**availability_type** | **str** | Identifies type of Delivery Window Availability. Values: &#x60;AVAILABLE&#x60;, &#x60;CONGESTED&#x60; | 
**delivery_window_option_id** | **str** | Identifier of a delivery window option. A delivery window option represent one option for when a shipment is expected to be delivered. | 
**editable_until** | **datetime** | The timestamp at which this Window can no longer be edited. | [optional] 
**end_date** | **datetime** | The end timestamp of the window. | 
**start_date** | **datetime** | The start timestamp of the window. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.selected_delivery_window import SelectedDeliveryWindow

# TODO update the JSON string below
json = "{}"
# create an instance of SelectedDeliveryWindow from a JSON string
selected_delivery_window_instance = SelectedDeliveryWindow.from_json(json)
# print the JSON string representation of the object
print(SelectedDeliveryWindow.to_json())

# convert the object into a dict
selected_delivery_window_dict = selected_delivery_window_instance.to_dict()
# create an instance of SelectedDeliveryWindow from a dict
selected_delivery_window_from_dict = SelectedDeliveryWindow.from_dict(selected_delivery_window_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


