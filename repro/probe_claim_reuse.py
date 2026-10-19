import independent_backend_probe as base
from django.test import TransactionTestCase
from django.test.utils import get_runner
from django.conf import settings
from fixtures.actors import make_student
from family_bridge_features.f04_ai.tests.test_f04 import grant_ai_consent
from family_bridge_features.f04_ai.services import registry
from family_bridge_features.f04_ai.services.express import AiExpressService
from family_bridge_features.f04_ai.models import AiSuggestion,AiRefineOperation
from family_bridge_features.f15_privacy.services import registry as privacy_registry
from family_bridge_features.f15_privacy.services.deletion import DeletionService
from family_bridge_core.idempotency import send_payload_hash

class ClaimReuseTests(TransactionTestCase):
    def test_old_result_cannot_finalize_a_recreated_claim_after_deletion(self):
        user=make_student();grant_ai_consent(user);uid=str(user.pk)
        key='audit-claim-reuse-0001';old_text='AUDIT_OLD_PRIVATE_BEFORE_DELETION';new_text='AUDIT_NEW_REQUEST_AFTER_DELETION'
        privacy_registry.register_deletion_hook('ai','family_bridge_features.f04_ai.services.deletion.AiSuggestionDeletionHook')
        states=[]
        class Provider:
            def refine(self,**kwargs):
                old_claim=AiRefineOperation.objects.get(author_id=uid,idempotency_key=key)
                d=DeletionService();r=d.request_deletion(user=user,categories=['ai'])
                d.verify_request(request_id=r['request_id'],verifier_ref='synthetic-local-verification')
                completed=d.process_request(request_id=r['request_id'])
                new_hash=send_payload_hash(kind='ai_refine',recipient_id='',body=new_text,reply_to=None,context_revision=2)
                # Deterministic interleaving: a new request claims the same
                # author/key after deletion, then its provider remains pending.
                AiExpressService()._claim_refine_operation(author_id=uid,idempotency_key=key,payload_hash=new_hash)
                new_claim=AiRefineOperation.objects.get(author_id=uid,idempotency_key=key)
                states.append({'deletion':completed.status,'claim_replaced':old_claim.pk!=new_claim.pk,'new_claim_payload_differs':new_claim.payload_hash_hex!=old_claim.payload_hash_hex})
                return {'suggested_text':'AUDIT_OLD_RESULT','provider_id':'local-test','model_revision':'test','prompt_revision':'test'}
        registry.register_ai_provider(Provider())
        try:
            AiExpressService().refine(author_id=uid,original_text=old_text,purpose='refine_expression',idempotency_key=key,input_revision=1)
        except Exception as e:states.append({'finalize_error':type(e).__name__})
        resurrected=AiSuggestion.objects.filter(author_id=uid,original_text=old_text).count()
        print('CLAIM_REUSE_EVIDENCE',states,'old_private_rows_after_deletion=',resurrected,flush=True)
        self.assertEqual(resurrected,0,'An old request must not own a recreated claim with the same key')

if __name__=='__main__':
    raise SystemExit(bool(get_runner(settings)(verbosity=2,interactive=False).run_tests(['__main__.ClaimReuseTests'])))
