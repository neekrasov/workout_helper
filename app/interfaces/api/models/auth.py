from dataclasses import dataclass


@dataclass
class LoginFormInputRequest:
    username: str
    password: str
