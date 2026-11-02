import unittest
from unittest.mock import AsyncMock, patch
import qimiao_client as client


class BoundaryTests(unittest.TestCase):
    def test_prohibited_actions_never_open_connection(self):
        for operation in ('pay_with_balance', 'connect_account', 'get_connected_account', 'create_order', 'quote_order', 'request_change', 'resume_order', 'cancel_order', 'https://example.invalid'):
            with self.subTest(operation=operation), patch.object(client, 'call_remote', new_callable=AsyncMock) as remote:
                self.assertTrue(client.invoke(operation).get('isError'))
                remote.assert_not_called()

    def test_invalid_or_oversized_arguments_never_open_connection(self):
        for raw in ('[]', 'null', '"string"', '{bad', 'x' * (1024 * 1024 + 1), '\u4e2d' * (400 * 1024)):
            with self.subTest(size=len(raw)), patch.object(client, 'call_remote', new_callable=AsyncMock) as remote:
                self.assertTrue(client.invoke('get_tool', raw).get('isError'))
                remote.assert_not_called()

    def test_sdk_exception_cannot_echo_task_credential(self):
        secret = 'private-credential-sentinel'
        with patch.object(client, 'call_remote', new_callable=AsyncMock, side_effect=RuntimeError(secret)):
            result = client.invoke('get_order', '{"credential":"' + secret + '"}')
        self.assertTrue(result.get('isError'))
        self.assertNotIn(secret, str(result))

    def test_nested_structured_response_and_failure_state_survive(self):
        payload = {'structuredContent': {'files': [{'format': 'pptx'}]}, 'content': [{'type': 'text', 'text': 'upstream failure'}], 'isError': True}
        with patch.object(client, 'call_remote', new_callable=AsyncMock, return_value=payload):
            self.assertEqual(client.invoke('get_tool', '{"tool_id":"ppt-maker"}'), payload)


if __name__ == '__main__':
    unittest.main()
