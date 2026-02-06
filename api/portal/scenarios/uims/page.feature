Feature: Page

  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Create a page and update its details

    When I create a page PID1
      | page_code | page_name | page_description | menu_category  | show_in_menu | menu_order | metadata                           |
      | it-page   | it page   | it page          | ADMIN CONTROLS | false        | 3          | {"env": "staging", "owner": "jay"} |

    When I create a widget WID1 with redirect_page none
      | widget_code            | widget_name | widget_description | widget_type | widget_sub_type | no_of_columns | widget_config     |
      | it-update-page-widget  | KPI Widget  | Shows KPI          | READ         | DETAILED       |4              | {"color": "green", "theme" : "white"} |

    When I create a page_widget_config PWCID1
      | page_widget_config_code| row_offset | column_offset | row_span | column_span |
      | it-page-widget-config  | 5          | 6             | 4        | 10          |

    Then I added widget WID1 to page PID1 with page_widget_config PWCID1

    Then I add page PID1 and widget WID1 to logged_in_user role

    Then I create a resource RID1 for portal with resource_code it-update-page-resource, widget WID1 and parent_resource as none

    Then I add resource RID1 and widget WID1 to logged_in_user role

    Then I update the page and verified updated details
      | page_code       | page_name      | page_description | menu_category  | show_in_menu | menu_order | metadata                                       |
      | it-update-page  | it update page | it update page   | ADMIN CONTROLS | false        | 5          | {"env": "staging update", "owner": "jay kumar"} |
