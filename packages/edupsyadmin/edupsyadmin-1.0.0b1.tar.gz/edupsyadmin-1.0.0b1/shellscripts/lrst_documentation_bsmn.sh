diagnosis=1
while getopts "n" flag; do
case "$flag" in
    n) diagnosis=0;;
esac
done

client_id=${@:$OPTIND:1}

if [ $diagnosis -eq 1 ]
then
edupsyadmin -w DEBUG \
    create_documentation $client_id\
    ~/Templates/Beratung/LRSt_GenehmigungSchulleitung_bsmn.pdf\
    ~/Templates/Beratung/LRSt_Stellungnahme_bsmn.pdf\
    ~/Templates/Beratung/LRSt_Informationsschreiben.pdf\
    ~/Templates/Beratung/LRSt_Anschreiben_bsmn.pdf\
    ~/Templates/Beratung/LRSt_AntragNachUeberpruefung_bsmn.pdf
else
edupsyadmin -w DEBUG \
    create_documentation $client_id\
    ~/Templates/Beratung/LRSt_StellungnahmeKeinBefund.pdf\
    ~/Templates/Beratung/LRSt_AnschreibenKeinBefund.pdf
fi
