# TransportationDetails

Transportation details for the shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_details** | [**List[TrackingDetails]**](TrackingDetails.md) | Tracking details for the shipment. If using SPD transportation, this can be for each case. If not using SPD transportation, this is a single tracking entry for the entire shipment. | 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.transportation_details import TransportationDetails

# TODO update the JSON string below
json = "{}"
# create an instance of TransportationDetails from a JSON string
transportation_details_instance = TransportationDetails.from_json(json)
# print the JSON string representation of the object
print(TransportationDetails.to_json())

# convert the object into a dict
transportation_details_dict = transportation_details_instance.to_dict()
# create an instance of TransportationDetails from a dict
transportation_details_from_dict = TransportationDetails.from_dict(transportation_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


