#!/usr/bin/env python3
__file__ = "PL2023_TPC5.sync.ipynb"

from dataclasses import dataclass
import re
import ply.lex as lex

# Define
BLOCKED: int = -2
ERROR: int = -1
SUCCESS: int = 0
BALANCE: int = 1
EXIT: int = 10

# List of token names.   This is always required
tokens: tuple[str] = ("LEVANTAR", "POUSAR", "MOEDA", "NUMERO", "ABORTAR")

# Regular expression rules for simple tokens
t_LEVANTAR: str = r"(?i)levantar"
t_POUSAR: str = r"(?i)pousar"
t_ABORTAR: str = r"(?i)abortar"

# A Regular Expression for phone numbers
def t_NUMERO(t):
    r"(?i)t=(\d+)"
    t.value = t.value[2:].strip()
    return t

# A Regular Expression for coins
def t_MOEDA(t):
    r"(?i)(moeda)(\s\d+[c|e],*)+"
    t.value = t.value.strip()
    t.value = re.sub(r"(?i)moeda ", "", t.value)
    t.value = re.sub(r",","", t.value)
    t.value = re.split(r"\s", t.value)
    return t

# A Regular Expression to ignore spaces, commas and points
def t_ignore_SPACE_POINT_COMMA(t):
    r"[ ,.]+"
    pass
    # No return value. Token discarded

# Track line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    #probably should handle this better
    print(f"Command not recognized: {t.value}")
    t.lexer.skip(len(t.value))

# Build the lexer
lexer = lex.lex()

# Allowed Coins 
usable_coins: list[str] = ["1c", "2c", "5c", "10c", "20c", "50c", "1e", "2e"]

# Value of each coin in cents
coin_values: dict[str, int] = {
    "1c": 1,
    "2c": 2,
    "5c": 5,
    "10c": 10,
    "20c": 20,
    "50c": 50,
    "1e": 100,
    "2e": 200,
}

# Blacklisted phone numbers
blacklist: list[str] = [r"^601", r"^641"]

# Phone Number identifier rules
phone_rules: dict[str, str] = {
    "International": r"\b00(?!351)",
    "National": r"\b00(?=351)",
    "Landline": r"\b2",
    "Emergency": r"\b112\b",
    "Mobile": r"\b9",
    "Green": r"\b800",
    "Blue": r"\b808",
}

# Phone Number call cost per identifier in cents
phone_prices: dict[str, int] = {
    "International": 150,
    "Landline": 25,
    "Emergency": 0,
    "Mobile": 35,
    "Green": 0,
    "Blue": 10,
}

# Convert cents to a string in the format "Xe Yc"
def from_cents_to_euros(cents: int) -> str:
    euros: int = cents // 100
    cents: int = cents % 100
    return f"{euros}e {cents}c"


# Class to represent the Telephone
@dataclass
class Telephone:
    state: bool
    coins: dict[str, int]
    balance: int
    wrong_coins: list[str]

    # __post_init__ sets all coins in the machine to 0
    def __post_init__(self):
        self.coins = {coin: 0 for coin in usable_coins}

    # The same as __str__
    def __repr__(self):
        return f"{'ON' if self.state else 'OFF'}\n{self.coins}\n{self.balance}"

    # Make a call
    def make_call(self, number: str) -> tuple[int, str]:
        if not self.state:
            return (ERROR, "Telephone is off")
        if re.match(phone_rules["Emergency"], number):
            return (SUCCESS, "Emergency call")

        if len(number) == 9 or (
            len(number) == 14 and (re.match(phone_rules["International"], number) or (re.match(phone_rules["National"], number)))):
            if re.match(phone_rules["National"], number):
                number = re.sub(r"\b00351","", number)
            if re.match(phone_rules["International"], number):
                if self.balance >= phone_prices["International"]:
                    self.balance -= phone_prices["International"]
                    return (SUCCESS, f"International call to {number}, Cost {from_cents_to_euros(phone_prices['International'])}")
                else:
                    return (BALANCE, "Not enough balance")
            elif re.match(phone_rules["Landline"], number):
                if self.balance >= phone_prices["Landline"]:
                    self.balance -= phone_prices["Landline"]
                    return (SUCCESS, f"Landline call to {number}, Cost {from_cents_to_euros(phone_prices['Landline'])}")
                else:
                    return (BALANCE, "Not enough balance")
            elif re.match(phone_rules["Mobile"], number):
                if self.balance >= phone_prices["Mobile"]:
                    self.balance -= phone_prices["Mobile"]
                    return (SUCCESS, f"Mobile call to {number}, Cost {from_cents_to_euros(phone_prices['Mobile'])}")
                else:
                    return (BALANCE, "Not enough balance")
            elif re.match(phone_rules["Green"], number):
                return (SUCCESS, f"Green call to {number}, Cost {from_cents_to_euros(phone_prices['Green'])}")
            elif re.match(phone_rules["Blue"], number):
                if self.balance >= phone_prices["Blue"]:
                    self.balance -= phone_prices["Blue"]
                    return (SUCCESS, f"Blue call to {number}, Cost {from_cents_to_euros(phone_prices['Blue'])}")
                else:
                    return (BALANCE, "Not enough balance")
            elif [True for rule in blacklist if re.match(rule, number)]:
                return (BLOCKED, "Blocked number")
            else:
                return (ERROR, "Unknown number")

        return (ERROR, "Invalid number")

    # Insert a coin into the machine
    def insert_coin(self, coin: str) -> tuple[int, str]:
        if not self.state:
            return (ERROR, "Telephone is off")
        if coin in self.coins.keys():
            self.coins[coin] += 1
            self.balance += coin_values[coin]
            return (SUCCESS, f"Coin inserted, {self.get_balance()[1]}")
        self.wrong_coins.append(coin)
        return (ERROR, f"Invalid coin {coin}, {self.get_balance()[1]}")

    # Turn the machine on
    def turn_on(self) -> tuple[int, str]:
        if self.state:
            return (ERROR, "Telephone is already on")
        self.state = True
        return (SUCCESS, "Telephone turned on, Plese insert coins")

    # Turn the machine off
    def turn_off(self) -> tuple[int, str]:
        if not self.state:
            return (ERROR, "Telephone is already off")
        self.state = False
        return (SUCCESS, f"Telephone turned off, {self.get_change_coins()[1]}" ) 

    # Get the balance of the machine
    def get_balance(self) -> tuple[int, str]:
        if not self.state:
            return (ERROR, "Telephone is off")
        return (SUCCESS, f"Balance: {self.balance//100}e {self.balance%100}c")

    # Get the coins inserted in the machine
    def get_coins(self) -> tuple[int, str]:
        if not self.state:
            return (ERROR, "Telephone is off")
        return (SUCCESS, f"Coins: {self.coins}")

    # Get machine state (on/off)
    def get_state(self) -> tuple[int, str]:
        return (SUCCESS, f"{'ON' if self.state else 'OFF'}")

    # Get the remaining balance
    def get_change(self) -> tuple[int, str]:
        if not self.state:
            return (ERROR, "Telephone is off")
        change = self.balance
        self.balance = 0
        self.coins = {coin: 0 for coin in usable_coins}
        return (SUCCESS, f"Change: {change}")

    # Abort the machine and return the coins, not changing the state
    def abort(self) -> tuple[int, str]:
        if not self.state:
            return (ERROR, "Telephone is off")
        self.coins = {coin: 0 for coin in usable_coins}
        return (SUCCESS, f"Operation aborted, {self.get_change_coins()[1]}")

    # Get wich coins are needed to return the remaining balance
    def calculate_change(self, change: int) -> dict[str, int]:
        coins = {coin: 0 for coin in usable_coins}
        for coin in reversed(usable_coins):
            while change >= coin_values[coin]:
                coins[coin] += 1
                change -= coin_values[coin]
        return coins

    # Get the coins needed to return the remaining balance
    def get_change_coins(self) -> tuple[int, str]:
        change = self.balance
        coins = self.calculate_change(self.balance)
        self.balance = 0
        self.coins = {coin: 0 for coin in usable_coins}
        coin_str: str = ", ".join([f"{coin}: {coins[coin]}" for coin in coins if coins[coin] > 0])
        return (SUCCESS, f"Change: {change//100}e {change%100}c, Coins: {coin_str}")


# Main function
def main():
    try:
        telephone: Telephone = Telephone(False, {}, 0,[])
        text: str = None
        result: tuple[int, str] = None
        ex: bool = False
        while not ex:
            try:
                text = input("OPERATION > ")
            except EOFError:
                text = ""
                ex = True
            if not text:
                text = ""
                ex = True
            lexer.input(text)
            while True:
                tok: lexer.token = lexer.token()
                if not tok:
                    break
                inv_coin: list[str] = []
                if tok and tok.type == "MOEDA":
                    coins: list[str] = tok.value
                    for coin in coins:
                        result = telephone.insert_coin(coin)
                        if result[0] != SUCCESS:
                            inv_coin.append(coin)
                            result = None
                if tok and tok.type == "LEVANTAR":
                    result = telephone.turn_on()
                if tok and tok.type == "NUMERO":
                    result = telephone.make_call(tok.value)
                if tok and tok.type == "POUSAR":
                    result = telephone.turn_off()
                    ex = True
                if tok and tok.type == "ABORTAR":
                    result = telephone.abort()
                if result or len(inv_coin) > 0:
                    invalid_coins = ""
                    if len(inv_coin) > 0:
                        invalid_coins = f", Invalid coins: {', '.join(inv_coin)}"
                    if not result:
                        result = telephone.get_balance()
                    print("maq:",result[1], invalid_coins)
    except KeyboardInterrupt as e:
        print("\nExit")


if __name__ == "__main__":
    main()
