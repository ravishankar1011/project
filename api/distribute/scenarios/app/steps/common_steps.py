import time

from behave import Step, use_step_matcher

use_step_matcher("re")
import tests.api.distribute.app.common.verify_mobile_number_steps
import tests.api.distribute.app.common.premium_account_steps
import tests.api.distribute.app.common.create_account_steps
import tests.api.distribute.app.common.account_steps
import tests.api.distribute.app.hugosave_sg.admin_steps
import tests.api.distribute.app.hugosave_sg.cash_map_steps
import tests.api.distribute.app.common.create_account_steps
import tests.api.distribute.app.hugobank_pk.credit_account_steps
import tests.api.distribute.app.hugosave_sg.device_tokens_steps
import tests.api.distribute.app.hugosave_sg.forgot_passcode_steps
import tests.api.distribute.app.hugosave_sg.intent_steps
import tests.api.distribute.app.hugosave_sg.map_schedule_steps
import tests.api.distribute.app.hugosave_sg.note_steps
import tests.api.distribute.app.hugosave_sg.payee_steps
import tests.api.distribute.app.hugosave_sg.physical_card_steps
import tests.api.distribute.app.hugosave_sg.plus_account_steps
import tests.api.distribute.app.hugosave_sg.questionnaire_steps
import tests.api.distribute.app.hugosave_sg.reward_steps
import tests.api.distribute.app.hugosave_sg.roundups_steps
import tests.api.distribute.app.hugosave_sg.update_details_steps
import tests.api.distribute.app.hugosave_sg.update_passcode
import tests.api.distribute.app.hugosave_sg.user_details
import tests.api.distribute.app.hugosave_sg.vault_steps
import tests.api.distribute.app.hugosave_sg.limits
import tests.api.distribute.app.hugosave_sg.spend_account_steps
import tests.api.distribute.app.common.account_management_steps
import tests.api.distribute.app.common.user_authorisation_token_steps
import tests.api.distribute.app.hugosave_sg.product_factory
import tests.api.distribute.app.hugobank_pk.qr_code_payments
import tests.api.distribute.app.common.device_authorisation_steps
import tests.api.distribute.app.hugobank_pk.bill_payments
import tests.api.distribute.app.hugobank_pk.document_centre_steps
import tests.api.distribute.app.hugobank_pk.virtual_id_steps
import tests.api.distribute.app.hugosave_sg.mandate_steps
import tests.api.distribute.app.hugobank_pk.credit_card

import tests.api.distribute.app.hugobank_pk.user_credi_test


@Step("I wait for ([^']*) seconds")
def wait_for(context, seconds):
    time.sleep(int(seconds))


# By default, behave ONLY look for step definitions in the root feature/steps directory
# If we put our files in subdirectories or directory outside feature/steps then behave will not recognize them
# As a work-around we can import all steps from all feature/<modules> in this file
# So the unused imports are not meant for removal from this common step module
