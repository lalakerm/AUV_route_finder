# Overview
The program simulates process of building optimal route for marine electric AUV (autonomous underwater vehicle)  
with given start and final coordinates with the usage of recharge points. All information about the vehicle and the route  
is written in the input file (see /data/input/input_data.txt). Program output consists of final report (as .pdf)  
with visual representation (also saves separately in .png file) and a list of control messages (NMEA-0183 protocol).  
Output examples are located in /data/output/.

# Tools
- Python v3.7
- numpy v1.16.0
- matplotlib v3.0.2
- fpdf v1.7.2

# Program usage
```
Template: NMEA_report_maker.py [options] [input_file] [output_path]  
Example: NMEA_report_maker.py -p \data\input\input_data.txt \data\output\  

Options:  
  -h, --help     show this help message and exit  
  -p, --picture  include graph picture [default: off]
```

# Mathematical model
[![bellmanford.png](https://i.postimg.cc/YS1xC3m7/bellmanford.png)](https://postimg.cc/mcg9d7wp)

# Output example
[![image.png](https://i.postimg.cc/V6sZN7LJ/image.png)](https://postimg.cc/sB8464Wz)

# NMEA-0183 description
NMEA is a standard text protocol, that's used in marine navigation equipment.  
Basic example of NMEA message:
$UTHDG, 15:21:04, 44.72, T, 206.57, E.
- $ - start delimiter
- UT - transmitter ID
- HDG - heading instruction
- 15:21:04 - time (UTC)
- 44.72 - distance (nm)
- T - turn instruction
- 206.57 - angle (degree)
- E - end of turn instruction
