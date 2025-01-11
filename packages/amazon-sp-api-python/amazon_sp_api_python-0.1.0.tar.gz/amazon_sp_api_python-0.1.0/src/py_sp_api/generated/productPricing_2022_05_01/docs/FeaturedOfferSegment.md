# FeaturedOfferSegment

Describes the segment in which the offer is featured.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_membership** | **str** | The customer membership type that makes up this segment | 
**segment_details** | [**SegmentDetails**](SegmentDetails.md) |  | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.featured_offer_segment import FeaturedOfferSegment

# TODO update the JSON string below
json = "{}"
# create an instance of FeaturedOfferSegment from a JSON string
featured_offer_segment_instance = FeaturedOfferSegment.from_json(json)
# print the JSON string representation of the object
print(FeaturedOfferSegment.to_json())

# convert the object into a dict
featured_offer_segment_dict = featured_offer_segment_instance.to_dict()
# create an instance of FeaturedOfferSegment from a dict
featured_offer_segment_from_dict = FeaturedOfferSegment.from_dict(featured_offer_segment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


