# Package

This object contains all the details of the scheduled Easy Ship package.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**scheduled_package_id** | [**ScheduledPackageId**](ScheduledPackageId.md) |  | 
**package_dimensions** | [**Dimensions**](Dimensions.md) |  | 
**package_weight** | [**Weight**](Weight.md) |  | 
**package_items** | [**List[Item]**](Item.md) | A list of items contained in the package. | [optional] 
**package_time_slot** | [**TimeSlot**](TimeSlot.md) |  | 
**package_identifier** | **str** | Optional seller-created identifier that is printed on the shipping label to help the seller identify the package. | [optional] 
**invoice** | [**InvoiceData**](InvoiceData.md) |  | [optional] 
**package_status** | [**PackageStatus**](PackageStatus.md) |  | [optional] 
**tracking_details** | [**TrackingDetails**](TrackingDetails.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.package import Package

# TODO update the JSON string below
json = "{}"
# create an instance of Package from a JSON string
package_instance = Package.from_json(json)
# print the JSON string representation of the object
print(Package.to_json())

# convert the object into a dict
package_dict = package_instance.to_dict()
# create an instance of Package from a dict
package_from_dict = Package.from_dict(package_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


