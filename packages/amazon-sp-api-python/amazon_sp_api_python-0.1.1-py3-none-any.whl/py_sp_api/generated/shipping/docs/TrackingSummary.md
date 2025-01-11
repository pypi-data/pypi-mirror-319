# TrackingSummary

The tracking summary.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | **str** | The derived status based on the events in the eventHistory. | [optional] 

## Example

```python
from py_sp_api.generated.shipping.models.tracking_summary import TrackingSummary

# TODO update the JSON string below
json = "{}"
# create an instance of TrackingSummary from a JSON string
tracking_summary_instance = TrackingSummary.from_json(json)
# print the JSON string representation of the object
print(TrackingSummary.to_json())

# convert the object into a dict
tracking_summary_dict = tracking_summary_instance.to_dict()
# create an instance of TrackingSummary from a dict
tracking_summary_from_dict = TrackingSummary.from_dict(tracking_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


