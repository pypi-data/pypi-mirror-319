# SegmentedFeaturedOffer

A product offer with segment information indicating where it's featured.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**seller_id** | **str** | The seller identifier for the offer. | 
**condition** | [**Condition**](Condition.md) |  | 
**sub_condition** | **str** | The item subcondition of the offer. | [optional] 
**fulfillment_type** | [**FulfillmentType**](FulfillmentType.md) |  | 
**listing_price** | [**MoneyType**](MoneyType.md) |  | 
**shipping_options** | [**List[ShippingOption]**](ShippingOption.md) | A list of shipping options associated with this offer | [optional] 
**points** | [**Points**](Points.md) |  | [optional] 
**prime_details** | [**PrimeDetails**](PrimeDetails.md) |  | [optional] 
**featured_offer_segments** | [**List[FeaturedOfferSegment]**](FeaturedOfferSegment.md) | The list of segment information in which the offer is featured. | 

## Example

```python
from py_sp_api.generated.productPricing_2022_05_01.models.segmented_featured_offer import SegmentedFeaturedOffer

# TODO update the JSON string below
json = "{}"
# create an instance of SegmentedFeaturedOffer from a JSON string
segmented_featured_offer_instance = SegmentedFeaturedOffer.from_json(json)
# print the JSON string representation of the object
print(SegmentedFeaturedOffer.to_json())

# convert the object into a dict
segmented_featured_offer_dict = segmented_featured_offer_instance.to_dict()
# create an instance of SegmentedFeaturedOffer from a dict
segmented_featured_offer_from_dict = SegmentedFeaturedOffer.from_dict(segmented_featured_offer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


