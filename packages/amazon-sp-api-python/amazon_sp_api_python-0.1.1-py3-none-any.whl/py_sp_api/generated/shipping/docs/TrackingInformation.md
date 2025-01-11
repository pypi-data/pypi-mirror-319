# TrackingInformation

The payload schema for the getTrackingInformation operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_id** | **str** | The tracking id generated to each shipment. It contains a series of letters or digits or both. | 
**summary** | [**TrackingSummary**](TrackingSummary.md) |  | 
**promised_delivery_date** | **datetime** | The promised delivery date and time of a shipment. | 
**event_history** | [**List[Event]**](Event.md) | A list of events of a shipment. | 

## Example

```python
from py_sp_api.generated.shipping.models.tracking_information import TrackingInformation

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingInformation from a JSON string
tracking_information_instance = TrackingInformation.from_json(json)
# print the JSON string representation of the object
print(TrackingInformation.to_json())

# convert the object into a dict
tracking_information_dict = tracking_information_instance.to_dict()
# create an instance of TrackingInformation from a dict
tracking_information_from_dict = TrackingInformation.from_dict(tracking_information_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


