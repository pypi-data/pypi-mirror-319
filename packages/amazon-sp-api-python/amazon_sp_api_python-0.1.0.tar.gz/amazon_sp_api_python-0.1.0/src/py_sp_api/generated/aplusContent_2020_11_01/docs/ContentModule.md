# ContentModule

An A+ Content module. An A+ Content document is composed of content modules. The contentModuleType property selects which content module types to use.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_module_type** | [**ContentModuleType**](ContentModuleType.md) |  | 
**standard_company_logo** | [**StandardCompanyLogoModule**](StandardCompanyLogoModule.md) |  | [optional] 
**standard_comparison_table** | [**StandardComparisonTableModule**](StandardComparisonTableModule.md) |  | [optional] 
**standard_four_image_text** | [**StandardFourImageTextModule**](StandardFourImageTextModule.md) |  | [optional] 
**standard_four_image_text_quadrant** | [**StandardFourImageTextQuadrantModule**](StandardFourImageTextQuadrantModule.md) |  | [optional] 
**standard_header_image_text** | [**StandardHeaderImageTextModule**](StandardHeaderImageTextModule.md) |  | [optional] 
**standard_image_sidebar** | [**StandardImageSidebarModule**](StandardImageSidebarModule.md) |  | [optional] 
**standard_image_text_overlay** | [**StandardImageTextOverlayModule**](StandardImageTextOverlayModule.md) |  | [optional] 
**standard_multiple_image_text** | [**StandardMultipleImageTextModule**](StandardMultipleImageTextModule.md) |  | [optional] 
**standard_product_description** | [**StandardProductDescriptionModule**](StandardProductDescriptionModule.md) |  | [optional] 
**standard_single_image_highlights** | [**StandardSingleImageHighlightsModule**](StandardSingleImageHighlightsModule.md) |  | [optional] 
**standard_single_image_specs_detail** | [**StandardSingleImageSpecsDetailModule**](StandardSingleImageSpecsDetailModule.md) |  | [optional] 
**standard_single_side_image** | [**StandardSingleSideImageModule**](StandardSingleSideImageModule.md) |  | [optional] 
**standard_tech_specs** | [**StandardTechSpecsModule**](StandardTechSpecsModule.md) |  | [optional] 
**standard_text** | [**StandardTextModule**](StandardTextModule.md) |  | [optional] 
**standard_three_image_text** | [**StandardThreeImageTextModule**](StandardThreeImageTextModule.md) |  | [optional] 

## Example

```python
from py_sp_api.generated.aplusContent_2020_11_01.models.content_module import ContentModule

# TODO update the JSON string below
json = "{}"
# create an instance of ContentModule from a JSON string
content_module_instance = ContentModule.from_json(json)
# print the JSON string representation of the object
print(ContentModule.to_json())

# convert the object into a dict
content_module_dict = content_module_instance.to_dict()
# create an instance of ContentModule from a dict
content_module_from_dict = ContentModule.from_dict(content_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


