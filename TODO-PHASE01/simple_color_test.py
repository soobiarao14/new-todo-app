#!/usr/bin/env python3
"""Simple test to verify colorama is working."""

from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

print("Testing colorama...")
print(Fore.RED + "This should be red")
print(Fore.GREEN + "This should be green")
print(Fore.BLUE + "This should be blue")
print(Fore.YELLOW + "This should be yellow")
print(Style.RESET_ALL + "This should be back to normal")
print("Colorama test completed!")