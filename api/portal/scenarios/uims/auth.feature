Feature: Auth

  Background:
    Given I logged in with credentials
      | username                     | password  |
      | mrityunjay.kumar@hugohub.com |           |

  Scenario: Refresh access token

    When I refresh access token for my account and I verify status code as 200
