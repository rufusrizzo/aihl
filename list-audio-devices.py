#!/home/riley/pvenv/bin/python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (C) 2025 Riley Chandler

# Additional note:
# If you're distributing this software, you must include the full text of the GPLv3 
# license either in the source code or in a separate file named LICENSE or COPYING.
#Original author RileyC started on 2/3/2025



import pyaudio

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']}")
    print(f"  Input Channels: {info['maxInputChannels']}")
    print(f"  Output Channels: {info['maxOutputChannels']}")
    print(f"  Default Sample Rate: {info['defaultSampleRate']}")
    print("---")

p.terminate()

