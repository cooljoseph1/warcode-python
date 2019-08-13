## Warcode 2019
Made by Joseph Camacho

## Table of Contents
[Introduction](#introduction)<br />
[Game Play](#game-play)<br />
[Passing data](#passing-data)<br />

<a name="introduction"></a>
## Introduction
Warcode is a real time strategy game.


<a name="game-play"></a>
## Game Play
The game is played by two or more AIs.    Each AI takes turns telling their units
to perform actions, ending when a certain number of rounds have been reached or
there is only one player left.

<a name="passing-data"></a>
## Passing data
The players and the engine communicate to each other through the player's
standard input and standard output.
Each turn the engine will print a **a single line** to the player's stdin and the
player must print out **a single line** to its stdout.
All data is sent as a json encoded string.
### Inputs
The player's first turn begins by the engine sending it the following json:
```
{
    "id": <team_id>,
    "num_players": <number_of_players>,
    "all_starting_locations": [
        [
            [<x>, <y>],
            ...
        ]
        ...
    ],
    "starting_locations": [
        [<x>, <y>],
        ...
    ]
    "map": <map>,
    "trees": <trees>,
    "gold_mines": <gold_mines>
}
```

Each successive turn will begin by the engine sending it json of the following
form:
```
{
    "units": {
        "<id_1>": {
            "type": <type>,
            "health": <health>,
            "team": <team_id>,
            "x": <x_position>,
            "y": <y_position>
        },
        ...
    }
    "map": <map>,
    "gold_mines": {
        "<id_1>": {
            "gold": <gold_left>,
            "x": <x_position>,
            "y": <y_position>
        },
        ...
    }
    "trees": {
        "<id_1>": {
            "wood": <wood_left>,
            "x": <x_position>,
            "y": <y_position>
        },
        ...
    }

}
```

### Outputs
The player ends his first turn by printing out its name (no json required here).
Note that any leading or trailing whitespace will be stripped from it.  A player
cannot take any actions on his first turn.  It is solely for any initialization
the player desires to do.

The player ends each successive turn by printing out json of the following form:
```
{
    actions: [
        <action_1>,
        ...
    ]
}
```
where `<action_1>`, `<action_2>`, etc. are certain actions described more below.

### Map
The empty map is sent as a two dimensional array, where each square is either an
integer from `0` to `2^32 - 1` or one of the characters `[I, B, E, G, T]`.  An
integer represents the id of the unit at that location.  The letters `I`, `B`,
`E`, `G`, and `T` represent an `INVISIBLE`, `BLOCK`, `EMPTY`, `GOLD_MINE`, or
`TREE` square, respectively.

### Actions
There are _ kinds of actions that a unit can do.  Each unit can only taken one
action per turn.  An illegal or incorrectly formatted action will be ignored
(and an error will be printed out by the engine if it is not running in quiet
mode)

The types of actions are:
#### Move
Moves a unit to a location.  Json format:
```
"move": {
    "unit": <unit_id>,
    "x": <x_position>,
    "y": <y_position>
}
```

#### Attack
Attacks a location.  Note that for totems to heal and mines to explode, they successive the "attack" command as well.  Json format:
```
"attack": {
    "unit": <unit_id>,
    "x": <x_position>,
    "y": <y_position>
}
```

#### Build
Builds a new unit.  Json format:
```
"build": {
    "unit": <unit_id>,
    "unit_type": <unit_type>,
    "x": <x_position>,
    "y": <y_position>
}
```

#### Give
Transfers resources from one unit to another unit.  Json format:
```
"give": {
    "unit": <unit_id>,
    "other": <other_id>,
    "gold": <gold>,
    "wood": <wood>
}
```

#### Cut
Cuts wood from a tree.  Json format:
```
"cut": {
    "unit": <unit_id>,
    "x": <x_position>,
    "y": <y_position>
}
```

#### Mine
Mines gold from a gold mine.  Json format:
```
"mine": {
    "unit": <unit_id>,
    "x": <x_position>,
    "y": <y_position>
}
```

#### Log
Logs a message.  Json format:
```
"log": {
    "message": <message>
}
```
