# ListTransportationOptionsResponse

The `listTransportationOptions` response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pagination** | [**Pagination**](Pagination.md) |  | [optional] 
**transportation_options** | [**List[TransportationOption]**](TransportationOption.md) | Transportation options generated for the placement option. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.list_transportation_options_response import ListTransportationOptionsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ListTransportationOptionsResponse from a JSON string
list_transportation_options_response_instance = ListTransportationOptionsResponse.from_json(json)
# print the JSON string representation of the object
print(ListTransportationOptionsResponse.to_json())

# convert the object into a dict
list_transportation_options_response_dict = list_transportation_options_response_instance.to_dict()
# create an instance of ListTransportationOptionsResponse from a dict
list_transportation_options_response_from_dict = ListTransportationOptionsResponse.from_dict(list_transportation_options_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


