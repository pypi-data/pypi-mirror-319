# DropOffLocation

The preferred location to leave packages at the destination address.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Specifies the preferred location to leave the package at the destination address. | 
**attributes** | **Dict[str, str]** | Additional information about the drop-off location that can vary depending on the type of drop-off location specified in the &#x60;type&#x60; field. If the &#x60;type&#x60; is set to &#x60;FALLBACK_NEIGHBOR_DELIVERY&#x60;, the &#x60;attributes&#x60; object should include the exact keys &#x60;neighborName&#x60; and &#x60;houseNumber&#x60; to provide the name and house number of the designated neighbor. | [optional] 

## Example

```python
from py_sp_api.generated.fulfillmentOutbound_2020_07_01.models.drop_off_location import DropOffLocation

# TODO update the JSON string below
json = "{}"
# create an instance of DropOffLocation from a JSON string
drop_off_location_instance = DropOffLocation.from_json(json)
# print the JSON string representation of the object
print(DropOffLocation.to_json())

# convert the object into a dict
drop_off_location_dict = drop_off_location_instance.to_dict()
# create an instance of DropOffLocation from a dict
drop_off_location_from_dict = DropOffLocation.from_dict(drop_off_location_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


