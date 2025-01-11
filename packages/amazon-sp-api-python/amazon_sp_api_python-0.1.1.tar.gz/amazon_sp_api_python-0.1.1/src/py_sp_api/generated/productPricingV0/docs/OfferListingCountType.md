# OfferListingCountType

The number of offer listings with the specified condition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | The number of offer listings. | 
**condition** | **str** | The condition of the item. | 

## Example

```python
from py_sp_api.generated.productPricingV0.models.offer_listing_count_type import OfferListingCountType

# TODO update the JSON string below
json = "{}"
# create an instance of OfferListingCountType from a JSON string
offer_listing_count_type_instance = OfferListingCountType.from_json(json)
# print the JSON string representation of the object
print(OfferListingCountType.to_json())

# convert the object into a dict
offer_listing_count_type_dict = offer_listing_count_type_instance.to_dict()
# create an instance of OfferListingCountType from a dict
offer_listing_count_type_from_dict = OfferListingCountType.from_dict(offer_listing_count_type_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


