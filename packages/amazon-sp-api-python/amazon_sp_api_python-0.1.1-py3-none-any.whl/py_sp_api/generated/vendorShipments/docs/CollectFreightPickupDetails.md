# CollectFreightPickupDetails

Transport Request pickup date from Vendor Warehouse by Buyer

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**requested_pick_up** | **datetime** | Date on which the items can be picked up from vendor warehouse by Buyer used for WePay/Collect vendors. | [optional] 
**scheduled_pick_up** | **datetime** | Date on which the items are scheduled to be picked from vendor warehouse by Buyer used for WePay/Collect vendors. | [optional] 
**carrier_assignment_date** | **datetime** | Date on which the carrier is being scheduled to pickup items from vendor warehouse by Byer used for WePay/Collect vendors. | [optional] 

## Example

```python
from py_sp_api.generated.vendorShipments.models.collect_freight_pickup_details import CollectFreightPickupDetails

# TODO update the JSON string below
json = "{}"
# create an instance of CollectFreightPickupDetails from a JSON string
collect_freight_pickup_details_instance = CollectFreightPickupDetails.from_json(json)
# print the JSON string representation of the object
print(CollectFreightPickupDetails.to_json())

# convert the object into a dict
collect_freight_pickup_details_dict = collect_freight_pickup_details_instance.to_dict()
# create an instance of CollectFreightPickupDetails from a dict
collect_freight_pickup_details_from_dict = CollectFreightPickupDetails.from_dict(collect_freight_pickup_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


