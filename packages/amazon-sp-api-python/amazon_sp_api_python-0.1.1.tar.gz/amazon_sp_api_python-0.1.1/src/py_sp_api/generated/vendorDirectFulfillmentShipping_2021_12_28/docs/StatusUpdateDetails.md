# StatusUpdateDetails

Details for the shipment status update given by the vendor for the specific package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tracking_number** | **str** | The shipment tracking number is required for every package and should match the &#x60;trackingNumber&#x60; sent for the shipment confirmation. | 
**status_code** | **str** | Indicates the shipment status code of the package that provides transportation information for Amazon tracking systems and ultimately for the final customer. For more information, refer to the [Additional Fields Explanation](https://developer-docs.amazon.com/sp-api/docs/vendor-direct-fulfillment-shipping-api-use-case-guide#additional-fields-explanation). | 
**reason_code** | **str** | Provides a reason code for the status of the package that will provide additional information about the transportation status. For more information, refer to the [Additional Fields Explanation](https://developer-docs.amazon.com/sp-api/docs/vendor-direct-fulfillment-shipping-api-use-case-guide#additional-fields-explanation). | 
**status_date_time** | **datetime** | The date and time when the shipment status was updated. Values are in [ISO 8601](https://developer-docs.amazon.com/sp-api/docs/iso-8601) date-time format, with UTC time zone or UTC offset. For example, 2020-07-16T23:00:00Z or 2020-07-16T23:00:00+01:00. | 
**status_location_address** | [**Address**](Address.md) |  | 
**shipment_schedule** | [**ShipmentSchedule**](ShipmentSchedule.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.vendorDirectFulfillmentShipping_2021_12_28.models.status_update_details import StatusUpdateDetails

# TODO update the JSON string below
json = "{}"
# create an instance of StatusUpdateDetails from a JSON string
status_update_details_instance = StatusUpdateDetails.from_json(json)
# print the JSON string representation of the object
print(StatusUpdateDetails.to_json())

# convert the object into a dict
status_update_details_dict = status_update_details_instance.to_dict()
# create an instance of StatusUpdateDetails from a dict
status_update_details_from_dict = StatusUpdateDetails.from_dict(status_update_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


