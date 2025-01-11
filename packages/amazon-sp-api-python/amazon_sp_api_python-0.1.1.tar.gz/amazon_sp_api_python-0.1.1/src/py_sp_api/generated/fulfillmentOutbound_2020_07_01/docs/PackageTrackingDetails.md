# PackageTrackingDetails

Tracking details of package

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_number** | **int** | The package identifier. | 
**tracking_number** | **str** | The tracking number for the package. | [optional] 
**customer_tracking_link** | **str** | Link on swiship.com that allows customers to track the package. | [optional] 
**carrier_code** | **str** | The name of the carrier. | [optional] 
**carrier_phone_number** | **str** | The phone number of the carrier. | [optional] 
**carrier_url** | **str** | The URL of the carrier&#39;s website. | [optional] 
**ship_date** | **datetime** | Date timestamp | [optional] 
**estimated_arrival_date** | **datetime** | Date timestamp | [optional] 
**ship_to_address** | [**TrackingAddress**](TrackingAddress.md) |  | [optional] 
**current_status** | [**CurrentStatus**](CurrentStatus.md) |  | [optional] 
**current_status_description** | **str** | Description corresponding to the &#x60;CurrentStatus&#x60; value. | [optional] 
**signed_for_by** | **str** | The name of the person who signed for the package. | [optional] 
**additional_location_info** | [**AdditionalLocationInfo**](AdditionalLocationInfo.md) |  | [optional] 
**tracking_events** | [**List[TrackingEvent]**](TrackingEvent.md) | An array of tracking event information. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.package_tracking_details import PackageTrackingDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PackageTrackingDetails from a JSON string
package_tracking_details_instance = PackageTrackingDetails.from_json(json)
# print the JSON string representation of the object
print(PackageTrackingDetails.to_json())

# convert the object into a dict
package_tracking_details_dict = package_tracking_details_instance.to_dict()
# create an instance of PackageTrackingDetails from a dict
package_tracking_details_from_dict = PackageTrackingDetails.from_dict(package_tracking_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


