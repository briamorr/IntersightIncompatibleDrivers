<h2>Example: Use API to determine if a server has incompatible drivers as well the supported versions from the HCL</h2>

<h2>Pre-reqs:</h2>

-Intersight API Keys

-Python 3.x

-Intersight Advantages licenses for HCL feature

<h2>Usage:</h2>

Modify serverMOID in incompatibledrivers.py to the server you wish to query

Modify api_key_id in incompatibledrivers.py to your API public key

Modify SecretKey.txt to your API private key

<br>
Example Output:


>#python incompatibledrivers.py

>

>Current HCL Status: Not-Listed

>Current Operating System: ESXi 6.7 U3


>Current Firmware Version: 4.1(3b)B

>Current Model: UCSB-B200-M3

>

>

>Component Status: Incompatible-Driver

>Model: UCSB-MLOM-40G-01

>Firmware: 4.4(1g)

>Driver Name: nenic

>Current Incompatible Driver Version: 1.0.29.0-1vmw.670.3.73.14320388

>Supported Driver Versions: 

>1.0.35.0-1OEM

>1.0.35.0-1OEM.670.0.0.8169922


<h2> Visualization From Intersight</h2>
<img src="Intesight UI.png"></img>
                                     
