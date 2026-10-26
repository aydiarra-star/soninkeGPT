import os
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from main import app


class ChatEndpointTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_chat_returns_503_without_server_key(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post("/api/chat", json={"message": "Bonjour"})
        self.assertEqual(response.status_code, 503)

    def test_chat_passes_corpus_context_and_mode_to_model(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="Réponse prudente."))
        ]
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), patch(
            "main.OpenAI", return_value=mock_client
        ):
            response = self.client.post(
                "/api/chat",
                json={
                    "message": "Que signifie ce mot ?",
                    "mode": "translation_vocabulary",
                    "corpus_context": "forme=borokaaxu; statut=validé par le référent",
                    "sources": [{"title": "Corpus local", "id": "entry-1"}],
                },
            )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["answer"], "Réponse prudente.")
        self.assertTrue(payload["corpus_context_used"])
        self.assertEqual(payload["sources"][0]["id"], "entry-1")
        call = mock_client.chat.completions.create.call_args.kwargs
        self.assertIn("statut=validé par le référent", call["messages"][0]["content"])
        self.assertIn("Ne fabrique jamais une forme soninkée", call["messages"][0]["content"])

    def test_chat_without_context_warns_about_unverified_forms(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value.choices = [
            MagicMock(message=MagicMock(content="Je ne peux pas confirmer la forme."))
        ]
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), patch(
            "main.OpenAI", return_value=mock_client
        ):
            response = self.client.post("/api/chat", json={"message": "Traduis-moi ceci"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["corpus_context_used"])
        self.assertIsNotNone(response.json()["warning"])

    def test_chat_rejects_unknown_mode_and_oversized_message(self):
        bad_mode = self.client.post(
            "/api/chat", json={"message": "Test", "mode": "magic"}
        )
        long_message = self.client.post(
            "/api/chat", json={"message": "x" * 4001}
        )
        self.assertEqual(bad_mode.status_code, 422)
        self.assertEqual(long_message.status_code, 422)


if __name__ == "__main__":
    unittest.main()
