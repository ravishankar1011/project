Feature: Spend account
  Background:
    Given I signup using bypass number
      | Casual Name | Legal Name | Email          | Passcode |
      | John        | Jones      | ns@12gmail.com | 111111   |
    When I wait for the premium upgrade to complete
    When I deposit amount using non prod options 500
    Given I tap on the spend account banner on the home screen
    When I tap on the Spend Account Dashboard Button and Close Announcement Modals

  Scenario: Top up the Spend Account
    When I top up the Spend Account with 100
    Then The Spend Account balance should reflect the 100.00

  Scenario: Withdraw from the Spend Account
    When I top up the Spend Account with 100
    Then The Spend Account balance should reflect the 100.00
    Then I withdraw 100 from the spend account
    Then The Spend Account balance should reflect the 00.00
