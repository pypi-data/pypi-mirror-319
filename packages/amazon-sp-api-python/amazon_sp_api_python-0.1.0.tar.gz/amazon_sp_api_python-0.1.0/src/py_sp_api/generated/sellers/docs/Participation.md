# Participation

Detailed information that is specific to a seller in a marketplace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_participating** | **bool** | If true, the seller participates in the marketplace. | 
**has_suspended_listings** | **bool** | If true, the seller has suspended listings. | 

## Example

```python
from py_sp_api.generated.sellers.models.participation import Participation

# TODO update the JSON string below
json = "{}"
# create an instance of Participation from a JSON string
participation_instance = Participation.from_json(json)
# print the JSON string representation of the object
print(Participation.to_json())

# convert the object into a dict
participation_dict = participation_instance.to_dict()
# create an instance of Participation from a dict
participation_from_dict = Participation.from_dict(participation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


