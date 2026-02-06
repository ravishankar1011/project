Feature: Create a schedule for metals
  Background:
    Given I signup using bypass number
      | Casual Name | Legal Name | Email          | Passcode |
      | Nas         | Nas SK     | ns@12gmail.com | 123456   |
    When I wait for the premium upgrade to complete
    When I deposit amount using non prod options 500
    When I move to the gold dashboard from the homescreen

  Scenario: I create a schedule with frequency and amount
    Given I create a schedule
      | Frequency | Week | Day | amount |
#      | Daily     |       |      | 100    |
#      | Weekly    |       | Tue  | 200    |
      | Monthly   | 4th  | Thu | 300    |


  #Scenario: I create a schedule for gold with daily frequency and tickle


#    When I click on the create schedule tab on the dashboard
#    When I select daily frequency
#    When I enter amount 50 and click on preview
#    When I click on the confirm schedule button
#    Then I validate daily text on the dashboard
#    When I move to the homescreen from the dashboard
#    When I tickle the schedule
#    When I move to the dashboard
#    Then I validate the transaction record on the dashboard
#
#
#
#
#
#  Scenario : I create a schedule for gold with weekly frequency
#
#  Scenario : I create a schedule for gold with monthly frequency
#
#  Scenario : I validate skip schedule functionality
#
#  Scenario : I validate stop schedule functionality