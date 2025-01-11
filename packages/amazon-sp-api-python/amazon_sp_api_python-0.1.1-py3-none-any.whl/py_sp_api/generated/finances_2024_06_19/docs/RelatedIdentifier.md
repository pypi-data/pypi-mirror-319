# RelatedIdentifier

Related business identifier of the transaction.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**related_identifier_name** | **str** | An enumerated set of related business identifier names. | [optional] 
**related_identifier_value** | **str** | Corresponding value of &#x60;RelatedIdentifierName&#x60;. | [optional] 

## Example

```python
from py_sp_api.generated.finances_2024_06_19.models.related_identifier import RelatedIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of RelatedIdentifier from a JSON string
related_identifier_instance = RelatedIdentifier.from_json(json)
# print the JSON string representation of the object
print(RelatedIdentifier.to_json())

# convert the object into a dict
related_identifier_dict = related_identifier_instance.to_dict()
# create an instance of RelatedIdentifier from a dict
related_identifier_from_dict = RelatedIdentifier.from_dict(related_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


