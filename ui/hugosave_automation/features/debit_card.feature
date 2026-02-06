Feature: Debit Card
  Background:
    Given I signup using bypass number
      | Casual Name | Legal Name | Email          | Passcode |
      | John        | Jones      | sara123@gmail.com | 111111   |
    When I wait for the premium upgrade to complete

  Scenario: Ordering a Debit Card
    Given I tap on the spend account banner on the home screen
    When I tap on the Spend Account Dashboard Button and Close Announcement Modals
    Given I open the Debit Card section from the Spend Account Dashboard
    Then I tap on the Confirm button to place the Debit Card order
    Then I should be redirected to the Card Dashboard with the ACTIVATE IT button visible

  Scenario: Activating the Debit Card
    Given I tap on the spend account banner on the home screen
    When I tap on the Spend Account Dashboard Button and Close Announcement Modals
    Given I open the Debit Card section from the Spend Account Dashboard
    Then I tap on the Confirm button to place the Debit Card order
    Then I should be redirected to the Card Dashboard with the ACTIVATE IT button visible
    When I tap on the ACTIVATE IT button and enter the token number 123456789
    Then I tap on the Activate Debit Card button to complete activation
    Then I tap on the GO TO CARD DASHBOARD button and verify the card is visible on the dashboard

  Scenario: Make a card transaction
    When I deposit amount using non prod options 500
    Given I tap on the spend account banner on the home screen
    When I tap on the Spend Account Dashboard Button and Close Announcement Modals
    When I top up the Spend Account with 100
    Then The Spend Account balance should reflect the 100.00
    Given I open the Debit Card section from the Spend Account Dashboard
    Then I tap on the Confirm button to place the Debit Card order
    Then I should be redirected to the Card Dashboard with the ACTIVATE IT button visible
    When I tap on the ACTIVATE IT button and enter the token number 123456789
    Then I tap on the Activate Debit Card button to complete activation
    Then I tap on the GO TO CARD DASHBOARD button and verify the card is visible on the dashboard
    Then I go to the home screen
    Then I go to non_prod options and make a auth_clear card transaction of 10
    Given I tap on the spend account banner on the home screen
    Then The Spend Account balance should reflect the 90.00
