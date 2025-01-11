# NonPartneredLtlDataInput

Information that you provide to Amazon about a Less Than Truckload/Full Truckload (LTL/FTL) shipment by a carrier that has not partnered with Amazon.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**carrier_name** | **str** | The carrier that you are using for the inbound shipment. | 
**pro_number** | **str** | The PRO number (\&quot;progressive number\&quot; or \&quot;progressive ID\&quot;) assigned to the shipment by the carrier. | 

## Example

```python
from py_sp_api.generated.fulfillmentInboundV0.models.non_partnered_ltl_data_input import NonPartneredLtlDataInput

# TODO update the JSON string below
json = "{}"
# create an instance of NonPartneredLtlDataInput from a JSON string
non_partnered_ltl_data_input_instance = NonPartneredLtlDataInput.from_json(json)
# print the JSON string representation of the object
print(NonPartneredLtlDataInput.to_json())

# convert the object into a dict
non_partnered_ltl_data_input_dict = non_partnered_ltl_data_input_instance.to_dict()
# create an instance of NonPartneredLtlDataInput from a dict
non_partnered_ltl_data_input_from_dict = NonPartneredLtlDataInput.from_dict(non_partnered_ltl_data_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


