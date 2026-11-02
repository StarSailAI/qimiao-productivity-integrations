import json
from pathlib import Path
import unittest
from unittest.mock import AsyncMock, patch

import yaml
import qimiao_client as client


class BoundaryTests(unittest.TestCase):
    def test_unknown_tool_names_never_open_connection(self):
        for operation in ('refund', 'recharge', 'transfer', 'https://example.invalid', '', None, ['create_order']):
            with self.subTest(operation=operation), patch.object(client, 'call_remote', new_callable=AsyncMock) as remote:
                self.assertTrue(client.invoke(operation).get('isError'))
                remote.assert_not_called()

    def test_invalid_or_oversized_arguments_never_open_connection(self):
        for raw in ('[]', 'null', '"string"', '{bad', 'x' * (1024 * 1024 + 1), '\u4e2d' * (400 * 1024)):
            with self.subTest(size=len(raw)), patch.object(client, 'call_remote', new_callable=AsyncMock) as remote:
                self.assertTrue(client.invoke('get_tool', raw).get('isError'))
                remote.assert_not_called()

    def test_sdk_exception_cannot_echo_task_or_account_credential(self):
        secret = 'private-credential-sentinel'
        with patch.object(client, 'call_remote', new_callable=AsyncMock, side_effect=RuntimeError(secret)):
            result = client.invoke('pay_with_balance', json.dumps({'credential': secret, 'connection_credential': secret}))
        self.assertTrue(result.get('isError'))
        self.assertNotIn(secret, str(result))

    def test_nested_response_payment_links_and_failure_state_survive(self):
        payload = {'structuredContent': {'files': [{'format': 'pptx'}], 'checkout_url': 'https://longxia.sale/example', 'contract': {'price_cents': 99}}, 'content': [{'type': 'text', 'text': 'upstream failure'}], 'isError': True}
        with patch.object(client, 'call_remote', new_callable=AsyncMock, return_value=payload):
            self.assertEqual(client.invoke('create_order', '{}'), payload)

    def test_balance_call_does_not_invent_confirmation_or_chain_actions(self):
        args = {'service_id': 'synthetic-service', 'credential': 'synthetic-task-secret', 'contract_id': 'frozen-contract', 'connection_id': 'synthetic-grant', 'connection_credential': 'synthetic-account-secret', 'request_key': 'fixed-order-request'}
        response = {'structuredContent': {'payment_state': 'awaiting_confirmation', 'confirmation_token': 'synthetic-token'}}
        with patch.object(client, 'call_remote', new_callable=AsyncMock, return_value=response) as remote:
            self.assertEqual(client.invoke('pay_with_balance', json.dumps(args)), response)
            remote.assert_awaited_once_with('pay_with_balance', args)
        self.assertNotIn('user_confirmation', args)

    def test_explicit_confirmation_and_idempotency_reach_upstream_unchanged(self):
        args = {'contract_id': 'frozen-contract', 'request_key': 'same-request-on-retry', 'confirmation_token': 'synthetic-token', 'user_confirmation': {'confirmed': True, 'amount_cents': 99, 'currency': 'CNY'}}
        with patch.object(client, 'call_remote', new_callable=AsyncMock, return_value={'isError': False}) as remote:
            for _ in range(2):
                client.invoke('pay_with_balance', json.dumps(args))
            self.assertEqual(remote.await_count, 2)
            for call in remote.await_args_list:
                self.assertEqual(call.args, ('pay_with_balance', args))

    def test_write_timeout_is_not_retried(self):
        with patch.object(client, 'call_remote', new_callable=AsyncMock, side_effect=TimeoutError()) as remote:
            self.assertTrue(client.invoke('create_order', '{"request_key":"same-request-on-retry"}').get('isError'))
            remote.assert_awaited_once()

    def test_tool_selector_has_exact_fixed_operation_scope(self):
        doc = yaml.safe_load((Path(client.__file__).parent / 'tools/qimiao_productivity.yaml').read_text())
        choices = {item['value'] for item in doc['parameters'][0]['options']}
        self.assertEqual(choices, client.ALLOWED | {'list_tools'})
        self.assertEqual(len(client.ALLOWED), 22)
        self.assertTrue({'quote_order', 'create_order', 'wait_order', 'request_change', 'resume_order', 'cancel_order', 'connect_account', 'pay_with_balance'} <= client.ALLOWED)

    def test_schema_discovery_does_not_auto_enable_future_upstream_operations(self):
        # Exercise the real client filtering with a fake SDK session/transport.
        from contextlib import asynccontextmanager
        from types import SimpleNamespace

        payload = {'tools': [{'name': name} for name in sorted(client.ALLOWED)] + [{'name': 'new_unreviewed_operation'}]}
        result = SimpleNamespace(model_dump=lambda **kwargs: payload.copy())
        session = AsyncMock()
        session.list_tools.return_value = result

        @asynccontextmanager
        async def transport(*args, **kwargs):
            yield (None, None, None)

        @asynccontextmanager
        async def session_context(*args, **kwargs):
            yield session

        with patch.object(client, 'streamable_http_client', transport), patch.object(client, 'ClientSession', session_context):
            value = client.invoke('list_tools')
        self.assertEqual({t['name'] for t in value['tools']}, client.ALLOWED)
        session.call_tool.assert_not_awaited()


if __name__ == '__main__':
    unittest.main()
