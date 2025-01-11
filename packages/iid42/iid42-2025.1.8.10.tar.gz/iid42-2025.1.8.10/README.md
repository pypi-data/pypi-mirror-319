# PyPI: IID42

PyPi: https://pypi.org/project/iid42

Sample:
```
# pip install iid42
import iid

# Send IID to a UDP Gate Relay
target = SendUdpIID("127.0.0.1",3615)
target.push_integer(42)
target.push_index_integer(2,42)
target.push_index_integer_date_local_now(0,42)
target.set_ntp_offset_tick(45453)
target.push_index_integer_date_ntp_now(0,42)
target.push_index_integer_date_ntp_in_seconds(0,42,1.25)
target.push_index_integer_date_ntp_in_milliseconds(0,42,250)

```


**IID**, short for **Index Integer Date**, is a 4/8/12/16-byte format designed for seamless communication across various network systems, including UDP, WebSocket, and Mirror.

By standardizing the code and API to work exclusively with integer values:
- It enables the creation of action index tables.
- It supports the development of specialized tools for specific tasks, allowing IID to facilitate remote actions effectively.

The **IID format** was developed to streamline QA testing across multiple devices and computers with precise timing coordination.

### Key Features of IID:
1. **Index on your own server**: Identifies the target device.
2. **Index on a shared server**: Identifies the user.
3. **Value**: Represents the transported integer value.
4. **Date**: Encoded in a specific `ulong` format:
   - **01.....TICK**: Sent using NTP time.
   - **02.....TICK**: Intended for execution at a designated NTP time.
   - **.......TICK**: Sent from an unknown source time but uses `DateTime.Now` in UTC since 1970.

If you need assistance or are interested in contributing to this project, feel free to reach out.  
Since 2024, all my tools have been built around this principle.

---

```
/*
 * ----------------------------------------------------------------------------
 * "PIZZA LICENSE":
 * https://github.com/EloiStree wrote this file.
 * As long as you retain this notice, you
 * can do whatever you want with this code.
 * If you think my code saved you time,
 * consider sending me a 🍺 or a 🍕 at:
 *  - https://buymeacoffee.com/apintio
 * 
 * You can also support my work by building your own DIY input device
 * using these Amazon links:
 * - https://github.com/EloiStree/HelloInput
 *
 * May the code be with you.
 *
 * Updated version: https://github.com/EloiStree/License
 * ----------------------------------------------------------------------------
 */
```



``` py
import os
import sys

if False:
    cmd = "pip install iid42 --force-reinstall"
    os.system(cmd)

import iid42
from iid42 import HelloWorldIID


HelloWorldIID.console_loop_to_push_iid_apintio()

```



``` py
import os
import sys

if False:
    cmd = "pip install iid42 --force-reinstall"
    os.system(cmd)

import iid42
from iid42 import SendUdpIID
import time

target = SendUdpIID("apint.ddns.net", 3615, use_ntp= True)
while True:
        # Request to press a key in 50 ms from now on ntp time
        target.push_bytes(iid42.iid_ms(0,1001,50))
        # Request to release it a key in 550 ms from now on ntp time
        target.push_bytes(iid42.iid_ms(0,2001,550))
        # Every 2 seconds
        time.sleep(2)
        t = time.time()+1000
        t_offset = t + target.ntp_offset_local_to_server_in_milliseconds
        print(f"TIME:{t} NTP:{t_offset}")

```
Use https://test.pypi.org for training.  
https://youtu.be/9Ii34WheBOA?t=699  
