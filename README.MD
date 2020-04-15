# Table of Contents
- [Station-Tools](#station-tools)
  * [Prerequisites](#prerequisites)
  * [Setting up your working environment](#setting-up-your-working-environment)
  * [installing packages](#installing-packages)
  * [Choosing the correct Python interpreter](#choosing-the-correct-python-interpreter)
  * [Usage](#usage)
  * [Data-manager.py](#data-managerpy)
    + [Inputs](#inputs)
    + [Outputs (3 files)](#outputs--3-files-)
  * [Localization.py](#localizationpy)
    + [Inputs](#inputs-1)
      - [Beep Filename and Path](#beep-filename-and-path)
      - [Node Filename and Path](#node-filename-and-path)
    + [Parameterization](#parameterization)
      - [Tag IDs](#tag-ids)
      - [Localization Frequencies](#localization-frequencies)
    + [Outputs](#outputs)
  * [Contributing](#contributing)
  * [License](#license)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>

# Station-Tools

Station-Tools is a set of Python programs used to manage and process your CTT SensorStation and CTT Node data into localization data (lat/long). 
 
## Prerequisites

Note: If you are familiar with Python, you can simply set up your own virtual environment with `Pandas`, `PIP Station-Tools`, and `PIP UTM`. `Anaconda` is an IDE that sets up these environments for you so you can get up and running without any Python experience. Therefore for this ReadMe we will assume you are going to install `Anaconda` and `VSC`. You'll need to install `Git` if it doesn't already exist, but `Pandas` will be installed for you when you install `Anaconda`.

Install the following:
* [Anaconda](https://www.anaconda.com/distribution/)
* [VSC](https://code.visualstudio.com/)
* [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/)


## Setting up your working environment

Once you've installed both Anaconda and VSC, close VSC and restart Anaconda and you should see VSC show up as an application in Anaconda. 

From within Anaconda click the **Launch** button for VSC.  
VSC will open.

From the Explorer menu in VSC

/Screen Shot 2020-04-09 at 9.47.26 PM.png

 click the **Clone Repository** button and clone the following repository to your computer.<br>

```https://github.com/bobfogg/sensor-station-tools```

## installing the station-tools and UTM packages


Open up a new terminal window by typing `^~`
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **station-tools** and **utm**.

```bash
pip install station-tools
pip install utm
```

## Choosing the correct Python interpreter

For Windows installs you can likely skip this step, but you may need to assign the correct Python interpreter with some operating systems (such as those running Mac OS X, for example) as VSC will often choose the default rather than the one installed be Anaconda. To do so is fairly easy (Thanks to Beaulin Twinkle at [My Tec Bits][ref]).

[ref]:  https://www.mytecbits.com/apple/macos/visual-studio-code-for-python-macos


1. Open the Command Palette by pressing the `Shift + Command + P` keys.
2. In the Command Palette, type in and select `Python: Select Interpreter`
3. From the list of interpreters, select the appropriate `Python 3.x` interpreter; it should indicate `Conda` or `Anaconda` in the name. This action will create folder `.vscode` inside your workspace. Inside this `.vscode` folder, you will now see a `settings.json` file which stores the settings specific to the workspace. In our case you'll find the Python interpreter path. 
4. Now visual studio is ready to interpret and run Python code.

## Usage

Within the sensor-station-tools GIT repository, there are several folders, including `station` and `tools`. You'll be working in `tools`, and specifically with the following two Python scripts: `data-manager.py` and `localization.py`. 

## Data-manager.py

`Data-manager.py` does exactly what is says- it manages the data from your SensorStation and merges those files into the files necessary to run the next script. You do not need to edit this script.

### Running the script


To run the script, return to the termial window (or open an new one by typing `^~`) and type the following code:

```py
python data_manager.py ./path.to.your.data.files/
```

The data_manager.py program will now run on the folder you specificed in the path, and will differentiate between `beep` `gps` and `node health` files so that the end result are three outputs.

### Outputs (3 files)


1. `station-beep-data.merged.yyyy-mm-dd.csv`
: This file represents all of the raw beeps from all tags detected by all nodes in the array for all hourly files in the home directory. These can be files that were not previously uploaded (rotated) and/or files that were  previously uploaded. In the case of duplicate files (as can occur if you have uncompressed some of the files but left the compressed files to remain in the home directory) duplicates will be dropped.<br><br>

2. `station-gps-data.merged.yyyy-mm-dd.csv`
: This file is a merge of all the GPS files. Note that if you are not moving your SensorStation, this will simply be a lot of redundant data. The GPS data is not used in the `localization.py` script.<br><br>

3. `station-health-data.merged.yyyy.mm.dd.csv`
: This file is a merge of all the Node Health files. These files are not used in the current version of `localization.py` but may be useful for evaluating node performance for the time periods being analyzed. For instance, you may want to think about weighting some node data more than others based on the number of times that node checked in relative to the others during the period of interest. While how to do so is outside the scope of this documentation, it is good to know that these data exist and where you can find them *(hint: in this file!)*.

## Localization.py

`Localization.py` will analyze the station-beep-data.merged file created by `Data.manager.py` and output localizations for each tag ID in the dataset over any number of time steps you specify.  The xxx method of localization is used here, which ignores RSSI in favor of beep frequency. Future versions will include a number of methods for localization calculation. To run this script requires some parameterization.
***
### Inputs

For this program you will be editing the code within the `Localization.py` file to modify the paths to various files, and parameterize the various analysis widows. Look for the code below within the program file.

```py
# EDIT BELOW #

# Update this to point to your merged beep data file 
beep_filename = 'station-beep-data.merged.yyyy-mm-dd.csv'
# node file with lat/lng data for node ids:  required NodeId,lat,lng fields
node_filename = 'node-locations.csv'
# Tag File Location - required fields:  TagId
tag_filename = 'tags-to-analyze.csv'

# STOP EDITING #
```

#### Beep Filename and Path


 Beep_filename = `path to station-beep-data.merged.YYYY-MM-DD_xxxxx.csv`
 
#### Node Filename and Path


 node_filename = `path to nodes.csv` file
 `nodes.csv` is a file that you must create that includes lat/long data for node IDs. The format of the csv must follow: `NodeId, lat, lng`. 
 
 `NodeID`
 : the unique serial ID assigned to the Node at delivery
 
 `lat`
 : latitude in decimal degrees using a geographic coordinate system of WGS84.
 
 `lng`
 : longitude id decimal degrees using a geographic coordinate system of WGS84.
 
 Additional fields are fine, but the first three must be as above and note that **field names are case-sensitive.**

#### Tag Filename and Path

The only requirement here is a single column named TagID (case sensitive). Any additional fields will be ignored, but will not cause a problem, so feel free to use files with additional fields.


`TagId`
: The 8-digit unique identifier that came with your LifeTag or PowerTag. Note that on V2 LifeTags you might see 10 digits. Only include the first 8 digits in this file, as the last two are a CRC and are not included in the datafile being analyzed. **Only data matching the tags listed in the file will be localized**.

#### Localization Frequencies


Here you have the option to run multiple localization frequencies simultaneously. At the end of the script you will find the frequency loop beginning with `freq = 60T`, which means localize at 60-minute intervals. The nomenclature is as follows:

	H = hours
	T = minutes
	S = seconds 
	ex: 30S, 1T, 5T, 15T, 30T, ...

You can therefore edit the frequency loop with as many variants as you wish, just realize that the time it will take to run through large datasets will likely be the limiting factor. 

```python
# YOU CAN EDIT BELOW #
# resample frequency for location estimates
# T=minutes, S=seconds, H=hours - ex:    30S, 60S, 1T, 5T, 15T, 30T, ...

freq = '60T'
for freq in ['5T', '15T', '30T', '60T', '120T']:
    get_locations(freq)

# STOP EDITING #
```

### Outputs


The output files will be time and date-stamped .csv files, one for each of the frequencies specified.

Each output file includes the following fields:


* `Time`
	* date/time stamp of beginning of frequency bin
* `lat`
	* latitude in decimal degrees, derived from trilateration over the specified time step (freq).
* `lng`
	* longitude in decimal degrees, derived from trilateration over the specified time step (freq).
* `easting`
	* easting in meters (based on the Universal Transverse Mercator projection (utm) )
* `northing`
	* northing in meters (based on the Universal Transverse Mercator projection (utm) )
* `count`
	* Number of unique beeps during the specified time step (freq).
* `unique_nodex`
	* Number of unique nodes which received the tag transmission over the specified time step (freq).
* `TagID`
	* The unique ID of the LifeTag or PowerTag
* `channel`
	* The channel from which these data were received. On stations with a single antenna, this will always be the same value, but in some cases where multiple antennas are detecting nodes, there could be more than one channel across a data file. In that case consider that there is redundant data present and filtering may be necessary when visualizing these data.
* `date`
	* the date during which these data were collected in `YYYY-MM-DD` format.
* `time_of_day`
	* The time of day during which these data were collected, rounded to the nearest hour in `HH:mm:ss` format.
* `hour`
	* The hour during which these data were collected in `hh` format.


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Cellular Tracking Technologies](http://celltracktech.com)