Feature: LOS service's End customer profile scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

  Scenario: Successful Onboarding of End Customer Profile

    Then I onboard Customer Profile Cid1 to LOS and verify onboard status as ONBOARD_SUCCESS

    Then I create below End-Customer-Profile
      | customer_identifier | customer_profile_identifier | end_customer_profile_identifier | first_name | last_name | region | email         | phone_number   |
      | Cid1                | CPid1                       | ECPid1                          | John       | Snow      | SG     | john@snow.com | +63 1234567890 |

    Then I onboard End Customer Profile ECPid1 to LOS and verify onboard status as ONBOARD_SUCCESS and status code as 200
