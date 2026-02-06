Feature: Widget Management

    Background:
        Given I logged in with credentials
            | username                      | password  |
            | mrityunjay.kumar@hugohub.com  | abcd      |

    Scenario: Create and update a widget with layout and config
        When I create a page PID1
            | page_code          | page_name    | page_description  | show_in_menu | metadata |
            | redirect-page-code-one | RedirectPage | test page         | false    | {"env": "staging", "owner": "jay"} |

        When I create a widget WID1 with redirect_page PID1
            | widget_code       | widget_name | widget_description | widget_type | widget_sub_type | no_of_columns  | widget_config |
            | it-widget-update  | KPI Widget  | Shows KPI          | READ        | DETAILED        | 4              | {"color": "green", "theme" : "white"}         |

        Then I update the widget_name, widget_description, widget_type, widget_sub_type, no_of_columns, widget_config of widget WID1 and verified updated details
            | widget_name       | widget_description    | widget_type | widget_sub_type | no_of_columns | widget_config     |
            | Updated name      | KPI dashboard updated | READ         | PAGINATED      | 6             | {"abc" : "dhhd"} |
