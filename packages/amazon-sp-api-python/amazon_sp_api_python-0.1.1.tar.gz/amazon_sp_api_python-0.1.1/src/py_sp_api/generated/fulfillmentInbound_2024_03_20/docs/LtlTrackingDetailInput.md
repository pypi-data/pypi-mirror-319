# LtlTrackingDetailInput

Contains input information to update Less-Than-Truckload (LTL) tracking information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bill_of_lading_number** | **str** | The number of the carrier shipment acknowledgement document. | [optional] 
**freight_bill_number** | **List[str]** | Number associated with the freight bill. | 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.ltl_tracking_detail_input import LtlTrackingDetailInput

# TODO update the JSON string below
json = "{}"
# create an instance of LtlTrackingDetailInput from a JSON string
ltl_tracking_detail_input_instance = LtlTrackingDetailInput.from_json(json)
# print the JSON string representation of the object
print(LtlTrackingDetailInput.to_json())

# convert the object into a dict
ltl_tracking_detail_input_dict = ltl_tracking_detail_input_instance.to_dict()
# create an instance of LtlTrackingDetailInput from a dict
ltl_tracking_detail_input_from_dict = LtlTrackingDetailInput.from_dict(ltl_tracking_detail_input_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


