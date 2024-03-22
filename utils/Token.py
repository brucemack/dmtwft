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
class Token:

    def __init__(self, text, row = 0, col = 0, is_quoted = False):
        self.text = text
        self.row = row
        self.col = col
        self.is_quoted = is_quoted

    def __repr__(self):
        if self.is_quoted:
            return "Token(\"" + self.text + "\")"
        else:
            return "Token(" + self.text + ")"

    def __eq__(self, other):
        return self.text == other.text and \
          self.is_quoted == other.is_quotec
