# ListingsItemPutRequest

The request body schema for the putListingsItem operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**product_type** | **str** | The Amazon product type of the listings item. | 
**requirements** | **str** | The name of the requirements set for the provided data. | [optional] 
**attributes** | **Dict[str, object]** | JSON object containing structured listings item attribute data keyed by attribute name. | 

## Example

```python
from py_sp_api.generated.listingsItems_2020_09_01.models.listings_item_put_request import ListingsItemPutRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListingsItemPutRequest from a JSON string
listings_item_put_request_instance = ListingsItemPutRequest.from_json(json)
# print the JSON string representation of the object
print(ListingsItemPutRequest.to_json())

# convert the object into a dict
listings_item_put_request_dict = listings_item_put_request_instance.to_dict()
# create an instance of ListingsItemPutRequest from a dict
listings_item_put_request_from_dict = ListingsItemPutRequest.from_dict(listings_item_put_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


