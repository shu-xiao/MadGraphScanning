#!/bin/bash

#scriptname=`basename $0`
#gzzhFactor=1
#mmed=$2
#mchi=$3
#gzzh=`echo $mmed*$gzzhFactor | bc -l`
procCardDir=procCards_bb
mkdir -p ${procCardDir}
name='ZpBaryonic_bb'
dirname=${name}_bannerDir
mkdir -p $dirname
mmed=100
mchi=100
gq=0.25
gzzhFactor=1
gzzh=$(echo $mmed*$gzzhFactor | bc -l)

#for ((mmed=100; mmed<=2000; mmed=mmed+100 ))
for gq in 0.25 0.5 0.75
do

    for ((mmed=100; mmed<=2000; mmed=mmed+100 ))
    do
        echo ""
        echo "Producing cards for mediator mass = "$mmed" GeV"
        echo "Producing cards for DM mass = "$mchi" GeV"
        echo "Producing cards for DM mass = "$mchi" GeV"
        echo "Producing cards for gzzH = "$gzzh" GeV"
        echo ""
        namegq=$(echo $gq*100|bc -l|awk '{printf("%d\n",$gq)}')
        newname=${name}\_MZp${mmed}\_gq${namegq}\_MDM${mchi}
        sed -e 's/ZBFOLDER/'$newname'/g' -e 's/gqu/'$gq'/g' -e 's/MMED/'$mmed'/g' -e 's/MCHI/'$mchi'/g' -e 's/gZZH/'$gzzh'/g' ZpBaryonic_bb_proc_card.dat > ${procCardDir}/${newname}_proc_card.dat
        #bsub -q2nw -R "rusage[mem=12000]" $PWD/runLaunch.sh $PWD $CARDSDIR/${newname}_proc_card.dat
        #$PWD/runLaunch.sh $PWD $CARDSDIR/${newname}_proc_card.dat
        #if [ -f ${dirname}/${newname}_banner.txt ]; then
        #    echo "continue "${newname}
        #    continue
        #fi
        ./bin/mg5_aMC  ${procCardDir}/${newname}_proc_card.dat
        cp ${newname}/Events/run_01/run_01_tag_1_banner.txt ${dirname}/${newname}_banner.txt
    done
done
