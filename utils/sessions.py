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
import uuid

# Where the session state is held
MAX_SESSIONS = 64
sessions = dict()
session_keys = list()

def set_max_sessions(s: int):
    global MAX_SESSIONS
    MAX_SESSIONS = s

def get_session_count():
    return len(sessions)

def get_session(session_key, default_maker = None):

    global MAX_SESSIONS

    if session_key is None:
        session_key = uuid.uuid4()

    if not session_key in sessions:
        if default_maker is None:
            raise Exception("Invalid session")
        sessions[session_key] = default_maker()
        sessions[session_key]["key"] = session_key
        session_keys.append(session_key)
        # Clean up if we have too many sessions
        while len(session_keys) > MAX_SESSIONS:
            oldest_key = session_keys.pop(0)
            sessions.pop(oldest_key)            

    return sessions[session_key]

