#!/bin/sh

IFS='
'

guidance=""
for l in `egrep 'FY|EPS|売上高|ガイダンス|発表|コンセンサス|サプライズ' $1`
do
	#echo $l
	case "$l" in
		*\$[A-Z][A-Z]* | *\$[A-Z][A-Z][A-Z]* | *\$[A-Z][A-Z][A-Z][A-Z]* )
			name=`echo $l | awk '{print $1}'`
			ticker=`echo $l | awk '{print $2}'`
			season=`echo $l | awk '{print $3}'`
			guidance=""
			echo -n "\n$name,$ticker,$season"
			;;
		*発表 )
			date=`echo $l | sed -e 's/発表//' | sed -e 's/ //g'`
			echo -n ",$date"
			;;
		*EPS* | *売上高* )
			type=`echo $l | sed -e 's/[①|②|③]//' | sed -e 's/太い大きな丸/ o/' | sed -e 's/バツ印/ x/'`

			echo -n ",$guidance$type"
			;;
		*ガイダンス* )
			type=`echo $l | sed -e 's/[①|②|③]//'`
			guidance=$type
			;;
		*∟発表\ * | *コンセンサス予想* | *サプライズ* )
			data=`echo $l | awk -F'：' '{print $2}' | sed -e 's/ //g' | sed -e 's/億/B/g'`
			echo -n ",$data"
			;;
		* )
			echo "others"
			;;
	esac
done
