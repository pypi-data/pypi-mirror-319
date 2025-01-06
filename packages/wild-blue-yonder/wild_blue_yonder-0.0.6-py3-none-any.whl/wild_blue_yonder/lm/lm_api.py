# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from functools import wraps
from datetime import datetime, timezone
from time import sleep
import requests


class GRQ():
    """
    rate limits headers https://console.groq.com/docs/rate-limits

    """
    session: requests.Session
    default_model = 'llama-3.1-8b-instant' # llama3-groq-70b-8192-tool-use-preview'

    LimitRequests       = 14400  # Requests Per Day (RPD)
    RemainingRequests   = 14400  # Requests Per Day (RPD)
    ResetRequests       = 6      # (s) Requests Per Day (RPD)
    LimitTokens         = 20000  # Tokens Per Minute (TPM)
    RemainingTokens     = 20000  # Tokens Per Minute (TPM)
    ResetTokens         = 60     # (ms) Tokens Per Minute (TPM)

    def __init__(self, *args, **kwargs):
        self.api_base       = environ.get('GROQ_API_BASE', 'https://api.groq.com/openai/v1')
        self.api_key        = environ.get('GROQ_API_KEY')
        self.default_model  = environ.get('GROQ_DEFAULT_MODEL', 'llama-3.1-8b-instant')

        self.session        = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json',
                                     'Authorization': 'Bearer ' + self.api_key})

    @staticmethod
    def _check_rate_limit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.RemainingRequests > 0:
                return func(self, *args, **kwargs)
            elif self.RemainingRequests == 0:
                sleep(6)
                return func(self, *args, **kwargs)
            else:
                raise RuntimeError(f'Rate limited, wait 6 seconds')
        return wrapper

    @_check_rate_limit
    def chat(self, messages, **kwargs):
        """A simple requests call to Groq chat completions endpoint.
                kwargs:
                    temperature     = 0 to 1.0
                    top_p           = 0.0 to 1.0
                    n               = 1 to ...
                    frequency_penalty = -2.0 to 2.0
                    presence_penalty = -2.0 to 2.0
                    max_tokens      = number of tokens
            """
        json_data = {
            'frequency_penalty':    kwargs.get('frequency_penalty', None),
            'logit_bias':           kwargs.get('logit_bias', None),
            'logprobs':             kwargs.get('logprobs', None),
            'max_tokens':           kwargs.get('max_tokens', 5),
            'messages':             kwargs.get('messages', messages),
            'model':                kwargs.get('model', self.default_model),
            'n':                    kwargs.get('n', 1),
            'parallel_tool_calls':  kwargs.get('parallel_tool_calls', True),
            'presence_penalty':     kwargs.get('presence_penalty', None),
            'response_format':      kwargs.get('response_format', None),
            'seed':                 kwargs.get('seed', None),
            'stop':                 kwargs.get('stop_sequences', ['stop']),
            'stream':               kwargs.get('stream', False),
            'stream_options':       kwargs.get('stream_options', None),
            'temperature':          kwargs.get('temperature', 0.5),
            'tool_choice':          kwargs.get('tool_choice', 'auto'),
            'tools':                kwargs.get('tools', None),
            'top_logprobs':         kwargs.get('top_logprobs', None),
            'top_p':                kwargs.get('top_p', 0.5),
            'user':                 kwargs.get('user', None)
        }
        try:
            response = self.session.post(
                f'{self.api_base}/chat/completions',
                json=json_data,
            )
            self._update_limits(response)

            if response.status_code == requests.codes.ok:
                result = response.json()
            else:
                print(f'Request status code: {response.status_code}')
                return None

            return result['choices'][0]['message']

        except Exception as e:
            print('Unable to generate ChatCompletion')
            print(f'Exception: {e}')
            return None

    def _update_limits(self, response: requests.Response):
        """
        """
        rh = response.headers
        self.LimitRequests          = int(rh['x-ratelimit-limit-requests'])  # Requests Per Day (RPD)
        self.RemainingRequests      = int(rh['x-ratelimit-remaining-requests'])  # Requests Per Day (RPD)
        self.LimitTokens            = int(rh['x-ratelimit-limit-tokens']) # Tokens Per Minute (TPM)
        self.RemainingTokens        = int(rh['x-ratelimit-remaining-tokens']) # Tokens Per Minute (TPM)
        self.ResetRequests          = int(rh['x-ratelimit-reset-requests'].replace('s', ''))  # Requests Per Day (RPD)
        self.ResetTokens            = int(rh['x-ratelimit-reset-tokens'].replace('ms', '')) # Tokens Per Minute (TPM)

    def yes_no(self, text: str, instructions: str = None, ):
        """
        """
        pass
