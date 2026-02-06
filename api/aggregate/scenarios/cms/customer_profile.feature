Feature: CMS service's Customer Profile scenarios

  Background: Set Customer Profile

    Given I set and verify customer Cid1, customer profile CPid1 in the context

  Scenario: Onboard Customer Profile

    Given I onboard HUGOHUB Customer Profile for CMS and verify onboard status as ONBOARD_SUCCESS

    Then I onboard Customer Profile Cid1 to CMS and verify onboard status as ONBOARD_SUCCESS

    Then I create the following transaction codes and verify status code is 200
      | transaction_code | iso_code | description            |
      | TXN1             | ISO1     | First transaction code |
      | TXN2             | ISO2     | Second one             |
      | TXN3             | ISO3     | Third transaction code |
      | TXN4             | ISO4     | Fourth one             |
