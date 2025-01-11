# TransportDetailInput

Information required to create an Amazon-partnered carrier shipping estimate, or to alert the Amazon fulfillment center to the arrival of an inbound shipment by a non-Amazon-partnered carrier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**partnered_small_parcel_data** | [**PartneredSmallParcelDataInput**](PartneredSmallParcelDataInput.md) |  | [optional] 
**non_partnered_small_parcel_data** | [**NonPartneredSmallParcelDataInput**](NonPartneredSmallParcelDataInput.md) |  | [optional] 
**partnered_ltl_data** | [**PartneredLtlDataInput**](PartneredLtlDataInput.md) |  | [optional] 
**non_partnered_ltl_data** | [**NonPartneredLtlDataInput**](NonPartneredLtlDataInput.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.transport_detail_input import TransportDetailInput

# TODO update the JSON string below
json = "{}"
# create an instance of TransportDetailInput from a JSON string
transport_detail_input_instance = TransportDetailInput.from_json(json)
# print the JSON string representation of the object
print(TransportDetailInput.to_json())

# convert the object into a dict
transport_detail_input_dict = transport_detail_input_instance.to_dict()
# create an instance of TransportDetailInput from a dict
transport_detail_input_from_dict = TransportDetailInput.from_dict(transport_detail_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


