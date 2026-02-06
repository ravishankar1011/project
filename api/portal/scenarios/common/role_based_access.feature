Feature: Role based page structure access

  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Fetching page structure based on role

    Given I create an api AID1 with api_code random and data_provider_id PORTAL with field FID1 with field_code random

    Given I create an api AID2 with api_code random and data_provider_id PORTAL with field FID1 with field_code random

    When I create a page PID1
      | page_code                      | page_name                      | page_description                | menu_category  | show_in_menu | menu_order | metadata                           |
      | it-role-based-page-access-one  | it role based page access one  | it role based page access one   | ADMIN CONTROLS | false        | 3          | {"env": "staging", "owner": "jay"} |

    When I create a page PID2
      | page_code                      | page_name                     | page_description              | menu_category  | show_in_menu | menu_order | metadata                             |
      | it-role-based-page-access-two  | it role based page access two | it role based access page two | ADMIN CONTROLS | false        | 3          | {"env": "staging", "owner": "hello"} |

    When I create a widget WID1 with redirect_page none
      | widget_code                    | widget_name                      | widget_description | widget_type | widget_sub_type | no_of_columns | widget_config                        |
      | it-role-based-page-access-one  | it role based page access one    | widget             | READ        | DETAILED        | 4             | {"env": "staging", "owner": "hello"} |

    When I create a widget WID2 with redirect_page none
      | widget_code                    | widget_name                      | widget_description | widget_type | widget_sub_type | no_of_columns | widget_config                        |
      | it-role-based-page-access-two  | it role based page access two    | widget             | READ        | DETAILED        | 4             | {"env": "staging", "owner": "hello"} |

    When I add data_source_id of api AID1 to widget WID1
      | operation_type |
      | READ_OPERATION |

    When I add data_source_id of api AID2 to widget WID2
      | operation_type |
      | READ_OPERATION |

    Given I create a page_widget_config PWCID1
      | page_widget_config_code                   | column_offset | row_offset | column_span | row_span |
      | integration-test-page-widget-config       | 4             | 4          | 4           | 4        |

    Then I added widget WID1 to page PID1 with page_widget_config PWCID1

    Then I added widget WID2 to page PID2 with page_widget_config PWCID1

    Then I add page PID1 and widget WID1 to logged_in_user role

    Then I try to fetch page structure of page PID1 with expected status code 200

    Then I try to fetch page structure of page PID2 with expected status code POSM_9302
