# DirectFulfillmentItemIdentifiers

Item identifiers for an item in a direct fulfillment shipment.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**line_item_id** | **str** | A unique identifier for an item provided by the client for a direct fulfillment shipment. This is only populated for direct fulfillment multi-piece shipments. It is required if a vendor wants to change the configuration of the packages in which the purchase order is shipped. | 
**piece_number** | **str** | A unique identifier for an item provided by the client for a direct fulfillment shipment. This is only populated if a single line item has multiple pieces. Defaults to 1. | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.direct_fulfillment_item_identifiers import DirectFulfillmentItemIdentifiers

# TODO update the JSON string below
json = "{}"
# create an instance of DirectFulfillmentItemIdentifiers from a JSON string
direct_fulfillment_item_identifiers_instance = DirectFulfillmentItemIdentifiers.from_json(json)
# print the JSON string representation of the object
print(DirectFulfillmentItemIdentifiers.to_json())

# convert the object into a dict
direct_fulfillment_item_identifiers_dict = direct_fulfillment_item_identifiers_instance.to_dict()
# create an instance of DirectFulfillmentItemIdentifiers from a dict
direct_fulfillment_item_identifiers_from_dict = DirectFulfillmentItemIdentifiers.from_dict(direct_fulfillment_item_identifiers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


