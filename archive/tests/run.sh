#!/bin/bash
# ./run.sh | wc -l should give 35 for now
(cd /root/MachineYadav/My-Tools/JScanner/tests || exit; fuser -k 80/tcp 1>/dev/null 2>/dev/null; php -S 0.0.0.0:80 1>/dev/null 2>/dev/null &)
(cd /root/MachineYadav/My-Tools/JScanner/tests || exit; JScanner -u http://localhost/example.js -o output/done1.txt -e)
(cd /root/MachineYadav/My-Tools/JScanner/tests || exit; JScanner -u http://localhost/example.html -o output/done2.txt -e)
