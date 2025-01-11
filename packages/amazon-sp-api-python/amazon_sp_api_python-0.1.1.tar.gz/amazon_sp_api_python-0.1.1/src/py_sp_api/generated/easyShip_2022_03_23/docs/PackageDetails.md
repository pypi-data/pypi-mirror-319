# PackageDetails

Package details. Includes `packageItems`, `packageTimeSlot`, and `packageIdentifier`.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**package_items** | [**List[Item]**](Item.md) | A list of items contained in the package. | [optional] 
**package_time_slot** | [**TimeSlot**](TimeSlot.md) |  | 
**package_identifier** | **str** | Optional seller-created identifier that is printed on the shipping label to help the seller identify the package. | [optional] 

## Example

```python
from py_sp_api.generated.easyShip_2022_03_23.models.package_details import PackageDetails

# TODO update the JSON string below
json = "{}"
# create an instance of PackageDetails from a JSON string
package_details_instance = PackageDetails.from_json(json)
# print the JSON string representation of the object
print(PackageDetails.to_json())

# convert the object into a dict
package_details_dict = package_details_instance.to_dict()
# create an instance of PackageDetails from a dict
package_details_from_dict = PackageDetails.from_dict(package_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


