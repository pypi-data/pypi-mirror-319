# ClassificationRefinement

Description of a classification that can be used to get more fine-grained search results.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number_of_results** | **int** | The estimated number of results that would still be returned if refinement key applied. | 
**display_name** | **str** | Display name for the classification. | 
**classification_id** | **str** | Identifier for the classification that can be used for search refinement purposes. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.classification_refinement import ClassificationRefinement

# TODO update the JSON string below
json = "{}"
# create an instance of ClassificationRefinement from a JSON string
classification_refinement_instance = ClassificationRefinement.from_json(json)
# print the JSON string representation of the object
print(ClassificationRefinement.to_json())

# convert the object into a dict
classification_refinement_dict = classification_refinement_instance.to_dict()
# create an instance of ClassificationRefinement from a dict
classification_refinement_from_dict = ClassificationRefinement.from_dict(classification_refinement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


