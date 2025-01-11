# EstimateTransportResponse

The response schema for the estimateTransport operation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CommonTransportResult**](CommonTransportResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.estimate_transport_response import EstimateTransportResponse

# TODO update the JSON string below
json = "{}"
# create an instance of EstimateTransportResponse from a JSON string
estimate_transport_response_instance = EstimateTransportResponse.from_json(json)
# print the JSON string representation of the object
print(EstimateTransportResponse.to_json())

# convert the object into a dict
estimate_transport_response_dict = estimate_transport_response_instance.to_dict()
# create an instance of EstimateTransportResponse from a dict
estimate_transport_response_from_dict = EstimateTransportResponse.from_dict(estimate_transport_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


