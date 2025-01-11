# GetCollectionFormHistoryRequest

The request schema to get query collections form history API .

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_reference_details** | [**List[ClientReferenceDetail]**](ClientReferenceDetail.md) | Object to pass additional information about the MCI Integrator shipperType: List of ClientReferenceDetail | [optional] 
**max_results** | **int** | max Number of Results for query . | [optional] 
**carrier_id** | **str** | The carrier identifier for the offering, provided by the carrier. | [optional] 
**ship_from_address** | [**Address**](Address.md) |  | [optional] 
**date_range** | [**DateRange**](DateRange.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.get_collection_form_history_request import GetCollectionFormHistoryRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GetCollectionFormHistoryRequest from a JSON string
get_collection_form_history_request_instance = GetCollectionFormHistoryRequest.from_json(json)
# print the JSON string representation of the object
print(GetCollectionFormHistoryRequest.to_json())

# convert the object into a dict
get_collection_form_history_request_dict = get_collection_form_history_request_instance.to_dict()
# create an instance of GetCollectionFormHistoryRequest from a dict
get_collection_form_history_request_from_dict = GetCollectionFormHistoryRequest.from_dict(get_collection_form_history_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


