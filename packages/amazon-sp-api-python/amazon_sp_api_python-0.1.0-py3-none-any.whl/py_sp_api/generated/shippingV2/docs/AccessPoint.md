# AccessPoint

Access point details

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_point_id** | **str** | Unique identifier for the access point | [optional] 
**name** | **str** | Name of entity (store/hub etc) where this access point is located | [optional] 
**timezone** | **str** | Timezone of access point | [optional] 
**type** | [**AccessPointType**](AccessPointType.md) |  | [optional] 
**accessibility_attributes** | [**AccessibilityAttributes**](AccessibilityAttributes.md) |  | [optional] 
**address** | [**Address**](Address.md) |  | [optional] 
**exception_operating_hours** | [**List[ExceptionOperatingHours]**](ExceptionOperatingHours.md) |  | [optional] 
**assistance_type** | **str** |  | [optional] 
**score** | **str** | The score of access point, based on proximity to postal code and sorting preference. This can be used to sort access point results on shipper&#39;s end. | [optional] 
**standard_operating_hours** | [**Dict[str, OperatingHours]**](OperatingHours.md) | Map of day of the week to operating hours of that day | [optional] 

## Example

```python
from py_sp_api.generated.shippingV2.models.access_point import AccessPoint

# TODO update the JSON string below
json = "{}"
# create an instance of AccessPoint from a JSON string
access_point_instance = AccessPoint.from_json(json)
# print the JSON string representation of the object
print(AccessPoint.to_json())

# convert the object into a dict
access_point_dict = access_point_instance.to_dict()
# create an instance of AccessPoint from a dict
access_point_from_dict = AccessPoint.from_dict(access_point_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


