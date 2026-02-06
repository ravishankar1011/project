Feature: Maker Checker flow

  Background:
    Given I logged in with credentials
      | username                     | password |
      | mrityunjay.kumar@hugohub.com | abcd     |

  Scenario: Perform maker-checker
    When I fetch all the permissions the logged-in user has

    Then I create a group GID1 with role none
      | group_name                           | description                          |
      | integration test maker-checker group | integration test maker-checker group |

    Then I create a role RID1 with all the permissions that the logged-in user has and add the checker group as GID1

    Then I update user role of user with user_id e143cf93-ebbf-46ca-8077-0de52c629c4f to RID1

    And I add user with user_id dfafca92-30a9-4f8b-a474-45a5d3707089 to group GID1

    Given I logged in with credentials
      | username                | password     |
      | shazeb.khan@hugohub.com | Admin@123456 |

    When I fetch my details

    Then I try to update my details

    Then I try to approve draft with expected status code POSM_9306

    Given I logged in with credentials
      | username                     | password        |
      | gitesh.singla@hugohub.com     | aTank@portal33 |

    Then I try to approve draft with expected status code 200
