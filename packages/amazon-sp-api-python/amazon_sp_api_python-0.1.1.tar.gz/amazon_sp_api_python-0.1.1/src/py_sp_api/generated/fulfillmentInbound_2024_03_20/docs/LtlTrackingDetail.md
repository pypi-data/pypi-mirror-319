# LtlTrackingDetail

Contains information related to Less-Than-Truckload (LTL) shipment tracking.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bill_of_lading_number** | **str** | The number of the carrier shipment acknowledgement document. | [optional] 
**freight_bill_number** | **List[str]** | The number associated with the freight bill. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentInbound_2024_03_20.models.ltl_tracking_detail import LtlTrackingDetail

# TODO update the JSON string below
json = "{}"
# create an instance of LtlTrackingDetail from a JSON string
ltl_tracking_detail_instance = LtlTrackingDetail.from_json(json)
# print the JSON string representation of the object
print(LtlTrackingDetail.to_json())

# convert the object into a dict
ltl_tracking_detail_dict = ltl_tracking_detail_instance.to_dict()
# create an instance of LtlTrackingDetail from a dict
ltl_tracking_detail_from_dict = LtlTrackingDetail.from_dict(ltl_tracking_detail_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


