Feature: Field

  Scenario: Successfully create and update field

    Given I create an api AID1 with api_code random and data_provider_id PORTAL with field FID1 with field_code random

    Then I create a field FID2 of api AID1 with field_code random and dependent_field none

    Then I create a field FID3 of api AID1 with field_code random and dependent_field FID2

    Then I updated field_name, field_description, field_type, data_type, group_by, is_edit_only, is_mandatory, field_order, is_paginated_field and dependent_field as FID2 of field FID3 and verified the updated details
      | field_name         | field_description         | field_type  | data_type | group_by   | is_edit_only  | is_mandatory | field_order | is_paginated_field |
      | updated field name | updated field description | IN_OUT      | BOOLEAN   | test-group | true          | true         | 1001        | true               |

     Then I updated the mapping path of the field FID3 and verified whether it was updated or not
      | request_mapping_path         | response_mapping_path      | request_field_position |
      | updated_request_mapping_path | updatedResponseMappingPath | QUERY                  |

    Then I updated the input config of the field FID3 and verified whether it was updated or not
      | component_type | is_immutable | placeholder     | default_value   | validation_type       | min_length | max_length | error_message            |
      | TEXT           | true         | Enter your name | Default Name    | STRING_VALIDATION     | 2          | 10         | Must be 2-10 characters. |

    Then I updated the output config of the field FID3 and verified whether it was updated or not
      | component_type | is_clickable | display_name    | action_type | modal_position | is_absolute_url |
      | FILE           | true         | Preview Brochure| VIEWABLE    | CENTER         | true            |

    Then I updated the effects of field FID3 where effects depends upon field FID2 and value is USER_ACTIVE and verified whether it was updated or not
