Feature: Money Market Fund module
  Background:
    Given I signup using bypass number
      | Casual Name | Legal Name | Email          | Passcode |
      | John        | Jones      | ns@12gmail.com | 111111   |
    When I wait for the premium upgrade to complete
    When I deposit amount using non prod options 500
    When I complete investment personality quiz from the homescreen

  Scenario: I buy mmf with balance in the save account
    When I move to the mmf dashboard from the homescreen
    When I click on the buy button
    When I enter amount 50 and click on preview
    When I click on the buy button
    Then I validate successfully bought message on the screen







