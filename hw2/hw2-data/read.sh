#!/bin/bash

while read line
do
    echo $line | carmel -sriIEQk 5 epron.wfsa epron-jpron.wfst > 4.5_result.txt
done < jprons.txt

echo 'H I R A R I K U R I N T O N' | carmel -sriIEQk 5 eword.wfsa eword-epron.wfst epron-jpron.wfst

echo 'H I R A R I K U R I N T O N' | carmel -sriIEQk 5 eword.wfsa eword-epron.wfst epron.wfsa epron-jpron.wfst

echo 'H I R A R I K U R I N T O N' | carmel -sriIEQk 5 eword.wfsa eword-epron.wfst epron-espell.wfst espell-eword.wfst eword-epron.wfst epron-jpron.wfst



T E I I S Y U 
interiachea

echo 'W H A L E B O N E S' | carmel -sriIEQk 5 epron.wfsa epron-espell.wfst