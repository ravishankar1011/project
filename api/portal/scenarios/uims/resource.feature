Feature: Resource

  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Successfully create and update a resource

    When I create a widget WID1 with redirect_page none
      | widget_code               | widget_name               | widget_description        | widget_type | widget_sub_type | no_of_columns | widget_config                           |
      | it-update-resource-widget | it update resource widget | it update resource widget | READ        | DETAILED        | 12            | {"color": "green", "theme" : "white"}   |

    Then I create a resource RID1 for portal with resource_code it-update-resource-one, widget WID1 and parent_resource as none

    Then I create a resource RID2 for portal with resource_code it-update-resource-two, widget WID1 and parent_resource as RID1

    Then I create a resource RID3 for portal with resource_code it-update-resource-three, widget WID1 and parent_resource as none

    Then I updated display_name, resource_description, parent_resource_code, param_type, dependent_on_resources, resource_order, is_mandatory, is_pinned of resource RID2 and parent_resource as RID3 and verified the updated details
      | display_name         | resource_description         | resource_type | parent_resource_code                                | dependent_on_resources                              | resource_order | is_mandatory | is_mandatory | is_pinned |
      | updated display name | updated resource description | OUTPUT        | it-update-resource-widget-it-dependent-resource-two | it-update-resource-widget-it-dependent-resource-two | 10000          | true         | true         | true      |

    Then I updated input_config of resource RID2 and verified the updated details
      | param_type | is_hidden | is_edit_only | sub_component_type | is_immutable | rule_type | min_length | max_length | placeholder | default_value |
      | IN_OUT     | true      | true         | TEXT               | true         | STRING_VALIDATION  | 1   | 100      | a placeholder | zyxw         |

    Then I updated output_config of resource RID2 and verified the updated details
      | sub_component_type | display_name | action_type | modal_position | is_absolute_url | is_concatenated | concatenated_pattern | show_in_table |
      | FILE               | download     | DOWNLOADABLE | BOTTOM        | true            | true            | abcd                 |  true           |

    Then I updated effects of resource RID2 where effects depends on resource RID3 and value is ACTIVE and verified the updated details

    Then I updated resource_layout_properties of resource RID2 and verified the updated details
      | key_layout_properties    | value_layout_properties   |
      | {"a": "bold"}            | {"x": 100, "y": true}     |
