# GiftDetails

Gift details for the item.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**gift_message** | **str** | Gift message to be printed in shipment. | [optional] 
**gift_wrap_id** | **str** | Gift wrap identifier for the gift wrapping, if any. | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentOrdersV1.models.gift_details import GiftDetails

# TODO update the JSON string below
json = "{}"
# create an instance of GiftDetails from a JSON string
gift_details_instance = GiftDetails.from_json(json)
# print the JSON string representation of the object
print(GiftDetails.to_json())

# convert the object into a dict
gift_details_dict = gift_details_instance.to_dict()
# create an instance of GiftDetails from a dict
gift_details_from_dict = GiftDetails.from_dict(gift_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


