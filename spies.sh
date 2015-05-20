#!/bin/bash

/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py --fresh 1.1 > spies.txt
/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py 1.2 >> spies.txt
/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py 1.4 >> spies.txt
/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py 1.5 >> spies.txt
/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py 1.6 >> spies.txt
/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py 1.7 >> spies.txt
/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py 07 >> spies.txt
/home/jon/work/python/virtualenvs/MontyLacuna/bin/python bin/spies_report.py 08 >> spies.txt

