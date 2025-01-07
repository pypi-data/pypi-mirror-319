from time import time_ns
from random import random
from uuid import uuid4

alphabet = '_-0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def generate_id() -> str:
  alphabet_len = len(alphabet)

  id = ''
  for _ in range(32):
      id += alphabet[int(random() * alphabet_len) | 0]
  return id

def generate_device_id() -> str:
  return f'$device:{uuid4()}'

def timestamp() -> int:
  return time_ns() // 1_000_000
