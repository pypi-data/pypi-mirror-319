# OutboundListing

A list of paginated outbound orders filtered by the attributes passed in the request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**next_token** | **str** | TA token that is used to retrieve the next page of results. The response includes &#x60;nextToken&#x60; when the number of results exceeds the specified &#x60;maxResults&#x60; value. To get the next page of results, call the operation with this token and include the same arguments as the call that produced the token. To get a complete list, call this operation until &#x60;nextToken&#x60; is null. Note that this operation can return empty pages. | [optional] 
**outbound_orders** | [**List[OutboundOrder]**](OutboundOrder.md) | List of outbound orders. | [optional] 

## Example

```python
from py_sp_api.generated.awd_2024_05_09.models.outbound_listing import OutboundListing

# TODO update the JSON string below
json = "{}"
# create an instance of OutboundListing from a JSON string
outbound_listing_instance = OutboundListing.from_json(json)
# print the JSON string representation of the object
print(OutboundListing.to_json())

# convert the object into a dict
outbound_listing_dict = outbound_listing_instance.to_dict()
# create an instance of OutboundListing from a dict
outbound_listing_from_dict = OutboundListing.from_dict(outbound_listing_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


