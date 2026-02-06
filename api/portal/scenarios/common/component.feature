Feature: Working of Dynamic Dropdown, file upload config, condition config
  Background:
    Given I logged in with credentials
      | username                     | password  |
      | mrityunjay.kumar@hugohub.com |           |

  Scenario: Verify working of dynamic dropdown, file upload config, condition config

    When I list all the the roles using dropdown resource view-operator-details-user-role-id of page view-operator-details and widget view-operator-details and I verify expected status code as 200

    When I fetch pre-signed-url using file upload config resource upload-user-documents-document-upload of page upload-user-documents and widget upload-user-documents and I verify expected status code as 200

    When I list all the conditions using condition config resource transaction-monitoring-create-rule-group-rule-group of page transaction-monitoring-create-rule-group and widget transaction-monitoring-create-rule-group and I verify expected status code as 200
