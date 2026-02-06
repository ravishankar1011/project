Feature: CMS service's Fund Transaction scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

    Given I onboard HUGOHUB Customer Profile for CMS and verify onboard status as ONBOARD_SUCCESS

    Then I onboard Customer Profile Cid1 to CMS and verify onboard status as ONBOARD_SUCCESS

  Scenario: Successful Fund Deposit to Customer Float Account.

    Then I deposit funds into the following funding account for Customer Profile and verify status code as 200
      | account_type | amount | currency |
      | FLOAT        | 1500   | SGD      |

  Scenario: Deposit With Amount greater than Decimal Digits permitted

    Then I deposit funds into the following funding account for Customer Profile and verify status code as E9500
      | account_type | amount   | currency |
      | FLOAT        | 1500.123 | SGD      |
