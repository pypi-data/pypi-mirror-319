# SegmentDetails

The details about the segment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**glance_view_weight_percentage** | **float** | The glance view weighted percentage for this segment, which is the glance views for this segment as a percentage of total glance views across all segments for the ASIN. A higher percentage indicates that more Amazon customers receive this offer as the Featured Offer. | [optional] 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.segment_details import SegmentDetails

# TODO update the JSON string below
json = "{}"
# create an instance of SegmentDetails from a JSON string
segment_details_instance = SegmentDetails.from_json(json)
# print the JSON string representation of the object
print(SegmentDetails.to_json())

# convert the object into a dict
segment_details_dict = segment_details_instance.to_dict()
# create an instance of SegmentDetails from a dict
segment_details_from_dict = SegmentDetails.from_dict(segment_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


