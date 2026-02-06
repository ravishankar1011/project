Feature: Api

  Scenario: Successfully add new fields to an existing API

    Given I create an api AID1 with api_code random and data_provider_id PORTAL with field FID1 with field_code random

    Then I add a new field FID2 with field_code random to api AID1 and dependent_field as FID1

    Then I fetch API AID1 and verify that field FID2 is present, and that field FID1 is a dependent field of FID2
