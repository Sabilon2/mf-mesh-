import os
import subprocess

ftyps = []
mdats = []

offset = 0

for filename in os.listdir('.'):
    if filename.endswith("_mdat.mov"):
        mdats.append(filename)
        continue
    if filename.endswith("_ftyp.mov"):
        ftyps.append(filename)
        continue

reverse = False
if reverse:
    ftyps = reversed(ftyps[offset:])
    mdats = reversed(mdats)
    outfile.write('echo -e "Image being searched in reverse, by request\n"')

ffounds = [
        ]
mfounds = [
        ]

fskips = 0
mskips = 0

with open('bashfile', 'w') as outfile:
    outfile.write("""#!/bin/bash
set -e

f_found=""
m_found=""

do_create() {
        outfile=$1
        dest="output/$outfile"
        mkdir -p output
        [ -f $dest ] && return
        ftyp=$2
        mdat=$3
        printf "$4 $5 - Testing $ftyp with $mdat...\\n"
        cat $ftyp $mdat > $dest
        jpeg="output/${outfile}.jpg"
        #printf "Creating screenshot to test video\\n"
        if ffmpeg -i $dest -vframes 1 -f image2 $jpeg -nostats -loglevel 0; then
            printf "\\033[1;32m$outfile: file succesfully recovered\\033[0m\\n"
        else
            truncate -s 0 $dest
        fi
}

exists () {
        #printf "Checking if result already exists for $1\\n"
        for f in output/*_$1[_.]*mov.jpg; do
                if [ -e "$f" ]; then
                       #printf "Found: $f\\n"
                       return 0
                fi
                #printf "Didn't find: $f\\n"
        done
        return 1
}

create () {
        i=$1
        f=$2
        ftyp=$3"_ftyp.mov"
        mdat=$4'_mdat.mov'
        outfile=$i"_"$f"_"$3"_"$4".mov"
        if exists $3; then
                if [ "$f_found" != "$3" ]; then
                        #printf "Skipping $outfile because result already found for ftyp: $3\\n"
                        f_found=$3
                fi
                return
        fi
        if exists $4; then
                if [ "$m_found" != "$4" ]; then
                        #printf "Skipping $outfile because result already found for mdat: $4\\n"
                        m_found=$4
                fi
                return
        fi
        do_create $outfile $ftyp $mdat $1 $2
}

""")
    for i, f in enumerate(ftyps[fskips:]):
        f_name = f.split('_')[0]
        if f_name in ffounds:
            print("Already found {} skipping".format(f_name))
            continue
        mds = mdats[i:] + mdats[:i]
        for j, m in enumerate(mds):  # Already got working copies of the first to mdats
            m_name = m.split('_')[0]
            
            if m_name in mfounds:
                print("Already found M {} skipping".format(m_name))
                continue
            output_name = '{}_{}_{}_{}.mov'.format(i+fskips, j+mskips, f_name, m_name)
            if reverse:
                output_name = 'test{}_{}_r.mov'.format(offset, i)
            outfile.write('create {} {} "{}" "{}"'.format(i, j, f_name, m_name))
            outfile.write("\n")

count = 0
for i in range(53):
    for i in range(53):
        count = count + 1
print(count)
