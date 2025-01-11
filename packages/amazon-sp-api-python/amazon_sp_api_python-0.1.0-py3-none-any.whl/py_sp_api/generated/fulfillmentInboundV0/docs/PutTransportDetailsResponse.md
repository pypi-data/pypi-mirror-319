# PutTransportDetailsResponse

Workflow status for a shipment with an Amazon-partnered carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**payload** | [**CommonTransportResult**](CommonTransportResult.md) |  | [optional] 
**errors** | [**List[Error]**](Error.md) | A list of error responses returned when a request is unsuccessful. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.put_transport_details_response import PutTransportDetailsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PutTransportDetailsResponse from a JSON string
put_transport_details_response_instance = PutTransportDetailsResponse.from_json(json)
# print the JSON string representation of the object
print(PutTransportDetailsResponse.to_json())

# convert the object into a dict
put_transport_details_response_dict = put_transport_details_response_instance.to_dict()
# create an instance of PutTransportDetailsResponse from a dict
put_transport_details_response_from_dict = PutTransportDetailsResponse.from_dict(put_transport_details_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


