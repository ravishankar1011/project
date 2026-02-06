Feature: Role based resource access
  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Role based resource access
    When I create a page PID1
      | page_code                      | page_name                  | page_description             | menu_category  | show_in_menu | menu_order | metadata                           |
      | it-role-based-resource-access  | role based resource access | role based resource access   | ADMIN CONTROLS | false        | 3          | {"env": "destroy", "owner": "jay"} |

    When I create a widget WID1 with redirect_page none
      | widget_code                    | widget_name                    | widget_description | widget_type | widget_sub_type | no_of_columns  | widget_config |
      | it-role-based-resource-access  | it role based resource access  | it widget          | READ        | DETAILED         | 4             |  {"env": "destroy", "owner": "jay"} |

    Given I create a page_widget_config PWCID1
      | page_widget_config_code                   | column_offset | row_offset | column_span | row_span |
      | integration-test-page-widget-config       | 4             | 4          | 4           | 4        |

    Given I added widget WID1 to page PID1 with page_widget_config PWCID1

    Then I add page PID1 and widget WID1 to logged_in_user role

    Then I create a resource RID1 for portal with resource_code it-role-based-resource-access-one, widget WID1 and parent_resource as none

    Then I create a resource RID2 for portal with resource_code random, widget WID1 and parent_resource as none

    Then I add resource RID1 and widget WID1 to logged_in_user role

    Then I fetched the page structure of page PID1 and verified that resource RID1 is present, while RID2 is not
