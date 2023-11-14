# Node Recorder

## Intro
Receiving odometry data and saving the node trajectory as CSV file.

## Running (node recording)
An odometry topic "odom" is required. The topic name can be changed at the below area:
https://github.com/hynkis/node_recorder/blob/4b78b9c7adc05a5990dbbae41335c7c18bf57a20/scripts/recorder.py#L98

`rosrun node_recorder recorder.py`

## Running (visualizing recorded data)
A marker topic "waypoint_node_markers" will be published.
https://github.com/hynkis/node_recorder/blob/4b78b9c7adc05a5990dbbae41335c7c18bf57a20/scripts/loader.py#L25

`rosrun node_recorder loader.py`

## Node class
You may manage the position (x,y), index, and score of each node using this class.
https://github.com/hynkis/node_recorder/blob/4b78b9c7adc05a5990dbbae41335c7c18bf57a20/scripts/recorder.py#L40-L45

## Node recording resolution
https://github.com/hynkis/node_recorder/blob/4b78b9c7adc05a5990dbbae41335c7c18bf57a20/scripts/recorder.py#L21
