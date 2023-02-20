#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from dataclasses import dataclass


# Machine class to store the state of the calculator
@dataclass
class Machine:
    counting:bool
    state:list[int]

    # Methods to turn the calculator on and off
    def turn_on(self) -> None:
        self.counting = True

    def turn_off(self) -> None:
        self.counting = False

    # Methods to add and get the state of the calculator
    def add_state(self, state:int) -> None:
        if self.counting:
            self.state.append(state)

    def get_state(self) -> int:
        return sum(self.state)

# Dictionary with the regex to be used
regex:dict = {
        "On":r"\b(on)\b",
        "Off":r"\b(off)\b",
        "Number":r"\b([0-9]+)\b",
        "Result":r"="
        }


def main():
    calculator:Machine = Machine(False, [])
    # Try to read the input and catch any exception
    try:
        # Loop to read the input
        shutdown:bool = False
        while not shutdown:
            line:str = input("-> ")
            #print(line)
            if line == "":
                shutdown = True
                continue
            line = line.split(" ")
            for word in line:
                if re.search(regex["On"], word, re.IGNORECASE):
                    calculator.turn_on()
                elif re.search(regex["Off"], word, re.IGNORECASE):
                    calculator.turn_off()
                elif re.search(regex["Number"], word, re.IGNORECASE):
                    calculator.add_state(int(word))
                elif re.search(regex["Result"], word, re.IGNORECASE):
                    print(f"Current State -> {calculator.get_state()}")
    # If an exception is caught, just ignore it and show the final state of the calculator
    except Exception:
        pass
    
    print("Closing calculator")
    print(f"Final state: {calculator.get_state()}")

if __name__ == "__main__":
    main()
