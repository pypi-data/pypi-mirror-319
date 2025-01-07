#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# Time       ：2025/1/4 11:05
# Author     ：Maxwell
# Description：
"""
import re
import base64
import json
import yaml
from pathlib import Path
from typing import Dict, Optional
from hwhkit.utils.security.rsa import RSACipher
from hwhkit.utils.security.aes import AESCipher
from hwhkit.connection.mqtt.plugins import PluginBase


class EncryptionPlugin(PluginBase):
    def __init__(self, key_pairs_file: str):
        self.topic_keys: Dict[str, Dict[str, str]] = {}
        self.load_key_pairs(key_pairs_file)

    def clean_key(self, key):
        return re.sub(r'\s+', '', key)

    def load_key_pairs(self, key_pairs_file: str):
        if not Path(key_pairs_file).exists():
            self.generate_default_yaml(key_pairs_file)

        with open(key_pairs_file, "r") as f:
            data = yaml.safe_load(f)
        if "key_pairs" not in data:
            raise ValueError("Invalid key_pairs file format: missing 'key_pairs' key")
        self.topic_keys = data["key_pairs"]

    def generate_default_yaml(self, key_pairs_file: str):
        rsa = RSACipher()
        default_data = {
            "key_pairs": {
                "default_topic": {
                    "public": rsa.serialize_public_key().decode('utf-8').strip(),
                    "private": rsa.serialize_private_key().decode('utf-8').strip()
                }
            }
        }
        with open(key_pairs_file, "w") as f:
            yaml.safe_dump(default_data, f)
        print(f"Generated default YAML file at: {key_pairs_file}")

    def get_keys(self, topic: str) -> Dict[str, str]:
        if topic not in self.topic_keys:
            raise ValueError(f"No keypair found for topic: {topic}")
        return self.topic_keys[topic]

    def on_message_published(self, topic: str, message: str) -> str:
        try:
            keys = self.get_keys(topic)
            public_key_pem = keys["public"]
            aes_cipher = AESCipher()
            aes_key = aes_cipher.get_key()
            public_key_pem_bytes = public_key_pem.encode('utf-8')
            public_key = RSACipher.deserialize_public_key(public_key_pem_bytes)
            rsa_cipher = RSACipher(public_key=public_key)
            encrypted_aes_key = rsa_cipher.encrypt(aes_key.encode('utf-8'))
            encrypted_message = aes_cipher.encrypt(message)

            payload = {
                "k": base64.b64encode(encrypted_aes_key).decode('utf-8'),
                "v": encrypted_message
            }
            return json.dumps(payload)
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")

    def on_message_received(self, topic: str, message: str) -> str:
        try:
            keys = self.get_keys(topic)
            private_key_pem = keys["private"]

            payload = json.loads(message)
            if 'k' not in payload or 'v' not in payload:
                raise ValueError("Invalid payload format")

            private_key_pem_bytes = private_key_pem.encode('utf-8')
            private_key = RSACipher.deserialize_private_key(private_key_pem_bytes)
            rsa_cipher = RSACipher(private_key=private_key)
            encrypted_aes_key = base64.b64decode(payload['k'].encode('utf-8'))
            aes_key = rsa_cipher.decrypt(encrypted_aes_key).decode('utf-8')

            aes_cipher = AESCipher(key=base64.b64decode(aes_key))
            return aes_cipher.decrypt(payload['v'])
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")