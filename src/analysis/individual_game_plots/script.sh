#!/bin/bash

SCENARIO="H"
ROUNDS=50
TURNS=100
PLAYERS=20

COOPERATIVE=19
GREEDY=0
RANDOM=0
ADVERSARIAL=1

# get current directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# concatenate DIR with "/scenario" and SCENARIO
NEW_DIR=$DIR/scenario_$SCENARIO

# create directory if it doesn't exist
mkdir -p $NEW_DIR

# iterate over .png files in this directory
for f in $DIR/*.png ; do
    # move file to DIR
    mv $f $NEW_DIR
done

# create a README.md where each line corresponds to the variables
# SCENARIO, ROUNDS, TURNS, PLAYERS, COOPERATIVE, GREEDY, RANDOM, ADVERSARIAL
echo "SCENARIO: $SCENARIO" > $NEW_DIR/README.md
echo "ROUNDS: $ROUNDS" >> $NEW_DIR/README.md
echo "TURNS: $TURNS" >> $NEW_DIR/README.md
echo "PLAYERS: $PLAYERS" >> $NEW_DIR/README.md
echo "COOPERATIVE: $COOPERATIVE" >> $NEW_DIR/README.md
echo "GREEDY: $GREEDY" >> $NEW_DIR/README.md
echo "RANDOM: $RANDOM" >> $NEW_DIR/README.md
echo "ADVERSARIAL: $ADVERSARIAL" >> $NEW_DIR/README.md