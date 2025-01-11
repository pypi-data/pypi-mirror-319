# ShipmentListing

A list of inbound shipment summaries filtered by the attributes specified in the request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | A token that is used to retrieve the next page of results. The response includes &#x60;nextToken&#x60; when the number of results exceeds the specified &#x60;maxResults&#x60; value. To get the next page of results, call the operation with this token and include the same arguments as the call that produced the token. To get a complete list, call this operation until &#x60;nextToken&#x60; is null. Note that this operation can return empty pages. | [optional] 
**shipments** | [**List[InboundShipmentSummary]**](InboundShipmentSummary.md) | List of inbound shipment summaries. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.shipment_listing import ShipmentListing

# TODO update the JSON string below
json = "{}"
# create an instance of ShipmentListing from a JSON string
shipment_listing_instance = ShipmentListing.from_json(json)
# print the JSON string representation of the object
print(ShipmentListing.to_json())

# convert the object into a dict
shipment_listing_dict = shipment_listing_instance.to_dict()
# create an instance of ShipmentListing from a dict
shipment_listing_from_dict = ShipmentListing.from_dict(shipment_listing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


