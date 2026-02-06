Feature: Working of Detailed Widget, Paginated Widget, Update Widget, Permission Widget, Menu widget, Detailed Read API, Paginated read API, Update API
  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com |          |

  Scenario: Verify working of paginated Widget using paginated API and Verify working of detailed widget using detailed API

    When I list all the the logs access_logs using paginated widget access-logs that call paginated api access-logs and I verify expected status code as 200

    Then I fetch details of one access log using detailed widget log-details that call detailed read API log-details and I verify expected status code as 200

  Scenario: Verify working of update widget and update API

    When I fetch my details user_details using update widget view-logged-in-operator-profile, detailed API get-logged-in-user-profile and verify expected status code as 200

    Then I update my details using update widget view-logged-in-operator-profile, update API update-logged-in-user-profile and verify updated details
      | first_name | last_name | phone_number |
      | random     | random    | random       |

  Scenario: Verify working of permission and menu widget

    When I list my permission using permission widget view-role-permissions and I verify expected status code as 200

    When I fetch menu widget menu-widget and I verify expected status code as 200

