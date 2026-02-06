Feature: Savings Pot

  Background:
	Given I sign up with bypass number
	  | prefix | name | place_of_birth | maiden_name |
	  | +9247  | Isha | Sector 17B     | Fernandez   |

  Scenario: I create a pot and choose to add money later
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name    | goal_amount | goal_date |
	  | Investments | 100.00      | today     |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details

  Scenario: I cancel the pot creation process in mid-way
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name    | goal_amount | goal_date |
	  | Investments | 100.00      |           |
	And I cancel the pot creation by clicking "Cancel" and confirming with "Yes"
	Then I Verify that navigated back to the savings pots dashboard

  Scenario: Create Pot with only pot name and goal amount
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name    | goal_amount | goal_date |
	  | Investments | 100.00      |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details

  Scenario: Create Pot with only pot name and goal date
	When I navigate to the savings pot dashboard
	When I create a new savings pot with the following details
	  | pot_name    | goal_amount | goal_date |
	  | Investments |             | today+3   |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details

  Scenario: Create Pot with only pot name
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name    | goal_amount | goal_date |
	  | Investments |             |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details

  Scenario: Create a savings pot with an invalid name
	When I navigate to the savings pot dashboard
	And I create a new savings pot with an invalid name "JVf%4$#%"
	Then the warning "Special characters not allowed" should be displayed the Next button should be disabled

  Scenario: I create a pot and choose to add 1 PKR immediately
	Given I have deposited 500 PKR into my account using non-prod options
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Movies   | 500         |           |
	And I complete the pot creation process by choosing "Yes, Add PKR 1"
	Then the pot should show a current balance of 1.00 PKR

  Scenario: I add amount to the pot
	Given I have deposited 500 PKR into my account using non-prod options
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Savings  | 200         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I add 10.00 PKR to the pot
	Then the pot should show a current balance of 10.00 PKR

  Scenario: Edit the savings pot name
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Deposits | 500         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I click on "Edit Pot Name" and I enter a new pot name as "Expenses"
	Then I verify that the pot name is updated to "Expenses"

  Scenario: withdraw amount from a savings pot
	Given I have deposited 500 PKR into my account using non-prod options
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Savings  | 200         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I add 100.00 PKR to the pot
	Then the pot should show a current balance of 100.00 PKR
	When I withdraw 50.00 PKR from the pot
	Then the pot should show a current balance of 50.00 PKR

  Scenario: Close a newly created savings pot
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | cats     | 500         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I open the pot's options menu and select Close, then confirm with Yes
	Then the pot should appear in the Closed Pots section with name "cats"

  Scenario: Create a savings pot and set up a schedule
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | cats     | 500         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	And I Click on Schedule Dashboard
	When I create a new schedule with the following details
	  | frequency | amount | start_date | make_payment | preview_button |
	  | Daily     | 200    | today      | Once         | enabled        |
	And I confirm the Schedule
	Then I verify the new schedule is displayed in the savings pot dashboard

  Scenario: Savings pot creation with schedule deletion
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | cats     | 500         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I create a new schedule with the following details
	  | frequency | amount | start_date | make_payment |
	  | Daily     | 200    | today      | Once         |
	Then I verify the new schedule is displayed in the savings pot dashboard
	Then I delete the schedule and confirm by selecting "Yes"
	Then I verify that the schedule has been deleted

  Scenario: Verify Stop & Resume Schedules are working
	Given I have deposited 500 PKR into my account using non-prod options
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | cats     | 500         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	And I Click on Schedule Dashboard
	When I create a new schedule with the following details
	  | frequency | amount | start_date | make_payment |
	  | Daily     | 200    | today      | Once         |
	Then I verify the new schedule is displayed in the savings pot dashboard
	And I stop the schedule and confirm by clicking "Yes"
	And I verify that the schedule has been "Stopped"
	And I Click on "Resume" to activate the schedule
	And I Verify that the schedule has been Activated

  Scenario: Create a pot after reached the pot's creation limit
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Pot 01   | 100.00      | today     |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I navigate to list of pots dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Pot 02   |             |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I navigate to list of pots dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Pot 03   |             | today     |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I navigate to list of pots dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Pot 04   | 100.00      | today     |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I navigate to list of pots dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Pot 05   | 100.00      | today     |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I navigate to list of pots dashboard
	Then I verify that "You have reached the limit!" text should appear

  Scenario: I Add amount to the pot greater than current account balance
	Given I have deposited 500 PKR into my account using non-prod options
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Savings  | 200         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	Then I add 600.00 PKR to the pot, then I should see "Insufficient balance in account"

  Scenario: Favourite and unfavourite the savings pot
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | Savings  |             |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	When I click the Favourite icon to mark the pot as Favourite
	Then the pot should appear in the list of Favourite pots on the dashboard
	When I click the Favourite icon again to remove it from Favourite
	Then The pot should no longer appear in the list of Favourite pots on the dashboard

  Scenario: I verify that Edit Schedule amount greater than 5,00,000 PKR is not possible
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | cats     | 500         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	And I Click on Schedule Dashboard
	When I create a new schedule with the following details
	  | frequency | amount | start_date | make_payment | preview_button |
	  | Daily     | 200    | today      | Once         | enabled        |
	And I confirm the Schedule
	Then I verify the new schedule is displayed in the savings pot dashboard
	And I "Edit" the scheduled amount as 500010 PKR
	Then I verify that schedule amount snap back to 500000

  Scenario: Verify schedule combinations and trigger schedule
	Given I have deposited 500 PKR into my account using non-prod options
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | cats     | 500         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	And I should see the new pot on the dashboard with correct details
	Given I click on Schedule Dashboard
	When I create a new schedule with the following details
		| frequency | amount | start_date | make_payment | preview_button |
		| Daily     | 200    | today+3    |              | disabled       |
		| Weekly    |        |            |              | disabled       |
		| Monthly   | 100    |            |              | disabled       |
		| Weekly    | 20     |            | Once         | disabled       |
		| Monthly   |        |            | Monthly      | disabled       |
		| Weekly    |        | today      | Twice        | disabled       |
		| Daily     | 100    | today      | Once         | enabled        |
	  When I confirm the Schedule
	And I verify the new schedule is displayed in the savings pot dashboard
	And I navigate to Homescreen
	And I trigger the schedule using non-prod options
	Then I verify that the schedule is triggered and amount 200.00 is settled

  Scenario: I validated that I have reached the goal for savings pot
	Given I have deposited 500 PKR into my account using non-prod options
	When I navigate to the savings pot dashboard
	And I create a new savings pot with the following details
	  | pot_name | goal_amount | goal_date |
	  | cats     | 200         |           |
	And I complete the pot creation process by choosing "I'll do it later"
	Then I should see the new pot on the dashboard with correct details
	And I add 500 PKR to the pot
	And the pot should show a current balance of 500.00 PKR
	Then I validated that "Goal Reached" Dialog is displayed