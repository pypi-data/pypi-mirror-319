# ListDeliveryWindowOptionsResponse

The `listDeliveryWindowOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delivery_window_options** | [**List[DeliveryWindowOption]**](DeliveryWindowOption.md) | Delivery window options generated for the placement option. | 
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_delivery_window_options_response import ListDeliveryWindowOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListDeliveryWindowOptionsResponse from a JSON string
list_delivery_window_options_response_instance = ListDeliveryWindowOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListDeliveryWindowOptionsResponse.to_json())

# convert the object into a dict
list_delivery_window_options_response_dict = list_delivery_window_options_response_instance.to_dict()
# create an instance of ListDeliveryWindowOptionsResponse from a dict
list_delivery_window_options_response_from_dict = ListDeliveryWindowOptionsResponse.from_dict(list_delivery_window_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


