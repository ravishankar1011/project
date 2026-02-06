Feature: File upload with maker checker enabled

  Background:
    Given I logged in with credentials
      | username                     | password  |
      | mrityunjay.kumar@hugohub.com |           |

  Scenario: Upload file with maker checker enabled

    When I fetch all the permissions the logged-in user has

    Then I create a group GID1 with role none
      | group_name                           | description                          |
      | integration test maker-checker group | integration test maker-checker group |

    Then I create a role RID1 with all the permissions that the logged-in user has and add the checker group as GID1

    Then I update user role of user with user_id d9cfe195-0072-4023-a8ca-318c34e24d47 to RID1

    And I add user with user_id a7d1802e-24f5-4d8a-8395-8a4c47f3cb2f to group GID1

    Given I logged in with credentials
      | username                | password     |
      | shazeb.khan@hugohub.com | Admin@123456 |

    Then I list all the users using widget user-profile-search for which we can upload file

    Then I try to upload a file using resource upload-user-documents-document-upload of widget upload-user-documents and page upload-user-documents and I verify expected status code as 200

    Then I try to process the file that uses resource upload-user-documents-document-upload of widget upload-user-documents and page upload-user-documents

    Then I try to approve draft with expected status code POSM_9306

    Given I logged in with credentials
      | username                     | password        |
      | gitesh.singla@hugohub.com     | aTank@portal33 |

    Then I try to approve draft with expected status code 200
