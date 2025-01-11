# NonPartneredLtlDataOutput

Information returned by Amazon about a Less Than Truckload/Full Truckload (LTL/FTL) shipment shipped by a carrier that has not partnered with Amazon.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **str** | The carrier that you are using for the inbound shipment. | 
**pro_number** | **str** | The PRO number (\&quot;progressive number\&quot; or \&quot;progressive ID\&quot;) assigned to the shipment by the carrier. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.non_partnered_ltl_data_output import NonPartneredLtlDataOutput

# TODO update the JSON string below
json = "{}"
# create an instance of NonPartneredLtlDataOutput from a JSON string
non_partnered_ltl_data_output_instance = NonPartneredLtlDataOutput.from_json(json)
# print the JSON string representation of the object
print(NonPartneredLtlDataOutput.to_json())

# convert the object into a dict
non_partnered_ltl_data_output_dict = non_partnered_ltl_data_output_instance.to_dict()
# create an instance of NonPartneredLtlDataOutput from a dict
non_partnered_ltl_data_output_from_dict = NonPartneredLtlDataOutput.from_dict(non_partnered_ltl_data_output_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


