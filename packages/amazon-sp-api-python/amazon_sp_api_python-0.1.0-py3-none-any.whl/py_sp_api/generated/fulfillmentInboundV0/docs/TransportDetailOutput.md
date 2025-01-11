# TransportDetailOutput

Inbound shipment information, including carrier details and shipment status.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**partnered_small_parcel_data** | [**PartneredSmallParcelDataOutput**](PartneredSmallParcelDataOutput.md) |  | [optional] 
**non_partnered_small_parcel_data** | [**NonPartneredSmallParcelDataOutput**](NonPartneredSmallParcelDataOutput.md) |  | [optional] 
**partnered_ltl_data** | [**PartneredLtlDataOutput**](PartneredLtlDataOutput.md) |  | [optional] 
**non_partnered_ltl_data** | [**NonPartneredLtlDataOutput**](NonPartneredLtlDataOutput.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.transport_detail_output import TransportDetailOutput

# TODO update the JSON string below
json = "{}"
# create an instance of TransportDetailOutput from a JSON string
transport_detail_output_instance = TransportDetailOutput.from_json(json)
# print the JSON string representation of the object
print(TransportDetailOutput.to_json())

# convert the object into a dict
transport_detail_output_dict = transport_detail_output_instance.to_dict()
# create an instance of TransportDetailOutput from a dict
transport_detail_output_from_dict = TransportDetailOutput.from_dict(transport_detail_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


