# BrandRefinement

Description of a brand that can be used to get more fine-grained search results.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number_of_results** | **int** | The estimated number of results that would still be returned if refinement key applied. | 
**brand_name** | **str** | Brand name. For display and can be used as a search refinement. | 

## Example

```python
from py_sp_api.generated.catalogItems_2022_04_01.models.brand_refinement import BrandRefinement

# TODO update the JSON string below
json = "{}"
# create an instance of BrandRefinement from a JSON string
brand_refinement_instance = BrandRefinement.from_json(json)
# print the JSON string representation of the object
print(BrandRefinement.to_json())

# convert the object into a dict
brand_refinement_dict = brand_refinement_instance.to_dict()
# create an instance of BrandRefinement from a dict
brand_refinement_from_dict = BrandRefinement.from_dict(brand_refinement_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


