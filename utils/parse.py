"""
* Copyright (C) 2024, Bruce MacKinnon KC1FSZ
*
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with this program.  If not, see <https://www.gnu.org/licenses/>.
*
* NOT FOR COMMERCIAL USE WITHOUT PERMISSION.
"""
from utils.Token import Token

def tokenize_line(line, row = 0):
    """
    Takes a line of text and breaks it into tokens.  This generally means 
    space-delimited, but quoted things are kept together.
    Also, the assignment operator is broken out into a token.
    """
    result = []
    in_delim = False
    in_quote = False
    last_token_quoted = False
    current_token = ""
    col = 0

    for c in line:

        col = col + 1

        if in_delim:
            if c == " ":
                pass
            elif c == "\"":
                in_quote = True
            elif c == ";":
                break
            # In the special case of =, that is a token in itself
            elif c == "=":
                result.append(Token("=", row, col))
                current_token = ""
                in_delim = False
            # This is the case where we end the delimiter and start 
            # accumulating a new token
            else:
                current_token = current_token + c
                in_delim = False
            
        elif in_quote:
            # This is the case where we close the quote and complete
            # a token
            if c == "\"":
                in_quote = False
                last_token_quoted = True
            # This is the case where we just keep accumulating a quoted
            # token.
            else:
                current_token = current_token + c
        else:
            # Look for the end of a complete token
            if c == " " or c == "=" or c == "*":
                if len(current_token) > 0:
                    result.append(Token(current_token, row, col, last_token_quoted))
                current_token = ""
                last_token_quoted = False

                # Space separates tokens (optionally)
                if c == " ":
                    in_delim = True
                # In the special case of = or *, that is a token in itself
                if c == "=":
                    result.append(Token("=", row, col))
                elif c == "*":
                    result.append(Token("*", row, col))

            # Look for the start of a quote
            elif c == "\"":
                in_quote = True
            # Comments end everything
            elif c == ";":
                break
            # Normal accumulation of a token
            else:
                current_token = current_token + c
    
    # Complete the the final token
    current_token = current_token.strip()
    if len(current_token) > 0:
        result.append(Token(current_token, row, col, last_token_quoted))

    return result 

def expand_tokens(named_constants, tokens):
    """
    Takes a list of tokens and returns a list of tokens after applying
    the substitutions of the named constants.  This is applied recursively
    since it is possible that some of the tokens in the named constant
    are themselves named constants.
    """
    # Resolve all named constants
    expanded_tokens = []
    for token in tokens:
        if token.text in named_constants:
            # NOTICE: We are recursive here to make sure that any constants
            # that are referenced inside of constant definitions are also 
            # expanded.
            for e in expand_tokens(named_constants, named_constants[token.text]):
                expanded_tokens.append(e)
        else:
            expanded_tokens.append(token)
    return expanded_tokens

def is_valid_dtmf_symbol(symbol):
    return symbol in [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#", "A", "B", "C", "D" ]

# Code assignments taken from S-COM documentation.
# NOTE: Prosigns are not supported at the moment

alpha_codes = dict()
alpha_codes["0"] = "00"
alpha_codes["1"] = "01" 
alpha_codes["2"] = "02"
alpha_codes["3"] = "03"
alpha_codes["4"] = "04"
alpha_codes["5"] = "05"
alpha_codes["6"] = "06"
alpha_codes["7"] = "07"
alpha_codes["8"] = "08"
alpha_codes["9"] = "09"
alpha_codes["A"] = "10"
alpha_codes["B"] = "11"
alpha_codes["C"] = "12"
alpha_codes["D"] = "13"
alpha_codes["E"] = "14"
alpha_codes["F"] = "15"
alpha_codes["G"] = "16"
alpha_codes["H"] = "17"
alpha_codes["I"] = "18"
alpha_codes["J"] = "19"
alpha_codes["K"] = "20"
alpha_codes["L"] = "21"
alpha_codes["M"] = "22"
alpha_codes["N"] = "23"
alpha_codes["O"] = "24"
alpha_codes["P"] = "25"
alpha_codes["Q"] = "26"
alpha_codes["R"] = "27"
alpha_codes["S"] = "28"
alpha_codes["T"] = "29"
alpha_codes["U"] = "30"
alpha_codes["V"] = "31"
alpha_codes["W"] = "32"
alpha_codes["X"] = "33"
alpha_codes["Y"] = "34"
alpha_codes["Z"] = "35"
alpha_codes["."] = "36"
alpha_codes[","] = "37"
alpha_codes["/"] = "38"
alpha_codes["?"] = "39"
alpha_codes[" "] = "40"
alpha_codes["-"] = "46"
alpha_codes[":"] = "47"
alpha_codes[";"] = "48"
alpha_codes["("] = "49"
alpha_codes[")"] = "49"
alpha_codes["'"] = "50"
alpha_codes["!"] = "51"
alpha_codes["\""]= "52"

def convert_token_to_dtmf_symbols(token):
    result = []
    eff_token = ""
    # For quoted tokens we need to map ASCII to the S-COM equivalent
    # codes.
    if token.is_quoted:
        # Take the token and convert each character
        for c in token.text:
            if c in alpha_codes:
                eff_token = eff_token + alpha_codes[c]
            else:
                raise Exception("Unable to convert quoted symbol to DTMF: " + c + " at line " + str(token.row))
    else:
        eff_token = token.text

    # Look at each character in the effective token and make sure it 
    # is a valid DTMF symbol
    for c in eff_token:
        if not is_valid_dtmf_symbol(c):
            raise Exception("Token \"" + token.text + "\" at line " + str(token.row) + " contains an invalid DTMF symbol: \"" + c + "\"")
        result.append(c)

    return result

def convert_tokens_to_dtmf_symbols(tokens):
    result = ""
    for token in tokens:
        result = result + convert_token_to_dtmf_symbols(token)
    return result
