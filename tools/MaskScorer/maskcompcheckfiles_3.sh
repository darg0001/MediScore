#!/bin/bash
clean=FALSE
procs=4

echo
echo "CASE 3: VALIDATING BIT-MASK SCORING"
echo

#TODO: design function to take test and output root as arguments and output total flag?

#produce the output files
python2 MaskScorer.py -t manipulation --refDir ../../data/test_suite/maskScorerTests/ -r reference/manipulation-image/MFC18-manipulation-image-ref.csv -x indexes/MFC18-manipulation-image-index.csv -s ../../data/test_suite/maskScorerTests/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1.csv -oR ../../data/test_suite/maskScorerTests/bittest_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1 --speedup -html -p $procs

#compare them to ground truth files
diff ../../data/test_suite/maskScorerTests/bittest_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_score.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_1.csv > comp_maskreport_bittest_1.txt
diff ../../data/test_suite/maskScorerTests/bittest_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_scores_perimage.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_1-perimage.csv > comp_maskreport_bittest_1-perimage.txt
diff ../../data/test_suite/maskScorerTests/bittest_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_journalResults.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_1-journalResults.csv > comp_maskreport_bittest_1-journalResults.txt

flag_bt1=1
flag_bt1pi=1
flag_bt1jr=1

filter_bt1="cat comp_maskreport_bittest_1.txt | grep -v CVS"
filter_bt1pi="cat comp_maskreport_bittest_1-perimage.txt | grep -v CVS"
filter_bt1jr="cat comp_maskreport_bittest_1-journalResults.txt | grep -v CVS"

if ([ ! -f comp_maskreport_bittest_1.txt -o ! -f comp_maskreport_bittest_1-journalResults.txt -o ! -f comp_maskreport_bittest_1-perimage.txt \
]); then
  echo
  echo "    !!!!! MASK SCORER TEST FAILED AT CASE 0 !!!!!    "
  echo "     MISSING FILES ABSENT FOR WHOLE BITTEST     "
  echo
  exit
fi

if test "`eval $filter_bt1`" = "" ; then
  flag_bt1=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_score.csv
	fi
	rm comp_maskreport_bittest_1.txt
else
	echo comp_maskreport_bittest_1.txt
	cat comp_maskreport_bittest_1.txt
fi

if test "`eval $filter_bt1pi`" = "" ; then
  flag_bt1pi=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_scores_perimage.csv
	fi
	rm comp_maskreport_bittest_1-perimage.txt
else
	echo comp_maskreport_bittest_1-perimage.txt
	cat comp_maskreport_bittest_1-perimage.txt
fi

if test "`eval $filter_bt1jr`" = "" ; then
  flag_bt1jr=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_journalResults.csv
	fi
	rm comp_maskreport_bittest_1-journalResults.txt
else
	echo comp_maskreport_bittest_1-journalResults.txt
	cat comp_maskreport_bittest_1-journalResults.txt
fi

bt1_total=$(($flag_bt1 + $flag_bt1pi + $flag_bt1jr))

#produce the output files
python2 MaskScorer.py -t manipulation --refDir ../../data/test_suite/maskScorerTests/ -r reference/manipulation-image/MFC18-manipulation-image-ref.csv -x indexes/MFC18-manipulation-image-index.csv -s ../../data/test_suite/maskScorerTests/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1.csv -oR ../../data/test_suite/maskScorerTests/bittest_partial/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1 --speedup -qm "Operation==['PasteSampled']" -p $procs

#compare them to ground truth files
diff ../../data/test_suite/maskScorerTests/bittest_partial/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_score.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_partial.csv > comp_maskreport_bittest_partial.txt
diff ../../data/test_suite/maskScorerTests/bittest_partial/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_scores_perimage.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_partial-perimage.csv > comp_maskreport_bittest_partial-perimage.txt
diff ../../data/test_suite/maskScorerTests/bittest_partial/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_journalResults.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_partial-journalResults.csv > comp_maskreport_bittest_partial-journalResults.txt

flag_btp=1
flag_btppi=1
flag_btpjr=1

filter_btp="cat comp_maskreport_bittest_partial.txt | grep -v CVS"
filter_btppi="cat comp_maskreport_bittest_partial-perimage.txt | grep -v CVS"
filter_btpjr="cat comp_maskreport_bittest_partial-journalResults.txt | grep -v CVS"

if ([ ! -f comp_maskreport_bittest_partial.txt -o ! -f comp_maskreport_bittest_partial-journalResults.txt -o ! -f comp_maskreport_bittest_partial-perimage.txt \
]); then
  echo
  echo "    !!!!! MASK SCORER TEST FAILED AT CASE 3 !!!!!    "
  echo "     MISSING FILES ABSENT FOR PARTIAL BITTEST     "
  echo
  exit
fi

if test "`eval $filter_btp`" = "" ; then
  flag_btp=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_partial/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_score.csv
	fi
	rm comp_maskreport_bittest_partial.txt
else
	echo comp_maskreport_bittest_partial.txt
	cat comp_maskreport_bittest_partial.txt
fi

if test "`eval $filter_btppi`" = "" ; then
  flag_btppi=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_partial/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_scores_perimage.csv
	fi
	rm comp_maskreport_bittest_partial-perimage.txt
else
	echo comp_maskreport_bittest_partial-perimage.txt
	cat comp_maskreport_bittest_partial-perimage.txt
fi

if test "`eval $filter_btpjr`" = "" ; then
  flag_btpjr=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_partial/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_journalResults.csv
	fi
	rm comp_maskreport_bittest_partial-journalResults.txt
else
	echo comp_maskreport_bittest_partial-journalResults.txt
	cat comp_maskreport_bittest_partial-journalResults.txt
fi

btp_total=$(($flag_btp + $flag_btppi + $flag_btpjr))

#produce the output files
python2 MaskScorer.py -t manipulation --refDir ../../data/test_suite/maskScorerTests/ -r reference/manipulation-image/MFC18-manipulation-image-ref.csv -x indexes/MFC18-manipulation-image-index.csv -s ../../data/test_suite/maskScorerTests/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1.csv -oR ../../data/test_suite/maskScorerTests/bittest_pixns/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1 --speedup -p $procs -pppns -html

#compare them to ground truth files
diff ../../data/test_suite/maskScorerTests/bittest_pixns/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_score.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_pixns.csv > comp_maskreport_bittest_pixns.txt
diff ../../data/test_suite/maskScorerTests/bittest_pixns/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_scores_perimage.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_pixns-perimage.csv > comp_maskreport_bittest_pixns-perimage.txt
diff ../../data/test_suite/maskScorerTests/bittest_pixns/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_journalResults.csv ../../data/test_suite/maskScorerTests/compcheckfiles/ref_maskreport_bittest_pixns-journalResults.csv > comp_maskreport_bittest_pixns-journalResults.txt

flag_btns=1
flag_btnspi=1
flag_btnsjr=1

filter_btns="cat comp_maskreport_bittest_pixns.txt | grep -v CVS"
filter_btnspi="cat comp_maskreport_bittest_pixns-perimage.txt | grep -v CVS"
filter_btnsjr="cat comp_maskreport_bittest_pixns-journalResults.txt | grep -v CVS"

if ([ ! -f comp_maskreport_bittest_pixns.txt -o ! -f comp_maskreport_bittest_pixns-journalResults.txt -o ! -f comp_maskreport_bittest_pixns-perimage.txt \
]); then
  echo
  echo "    !!!!! MASK SCORER TEST FAILED AT CASE 3 !!!!!    "
  echo "     MISSING FILES ABSENT FOR PARTIAL BITTEST     "
  echo
  exit
fi

if test "`eval $filter_btns`" = "" ; then
  flag_btns=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_pixns/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_score.csv
	fi
	rm comp_maskreport_bittest_pixns.txt
else
	echo comp_maskreport_bittest_pixns.txt
	cat comp_maskreport_bittest_pixns.txt
fi

if test "`eval $filter_btnspi`" = "" ; then
  flag_btnspi=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_pixns/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_mask_scores_perimage.csv
	fi
	rm comp_maskreport_bittest_pixns-perimage.txt
else
	echo comp_maskreport_bittest_pixns-perimage.txt
	cat comp_maskreport_bittest_pixns-perimage.txt
fi

if test "`eval $filter_btnsjr`" = "" ; then
  flag_btnsjr=0
	if [ $clean = "TRUE" ] ; then
		rm ../../data/test_suite/maskScorerTests/bittest_pixns/B_MFC18_Unittest_Manipulation_ImgOnly_p-me_1_journalResults.csv
	fi
	rm comp_maskreport_bittest_pixns-journalResults.txt
else
	echo comp_maskreport_bittest_pixns-journalResults.txt
	cat comp_maskreport_bittest_pixns-journalResults.txt
fi

btns_total=$(($flag_btns + $flag_btnspi + $flag_btnsjr))

flag_total=$(($bt1_total + $btp_total + $btns_total))

if ([ $flag_total -eq 0 ]); then
  echo
  echo "CASE 3 SUCCESSFULLY PASSED"
  echo
	if [ $clean = "TRUE" ] ; then
		rm -rf ../../data/test_suite/maskScorerTests/bittest_1
		rm -rf ../../data/test_suite/maskScorerTests/bittest_partial
		rm -rf ../../data/test_suite/maskScorerTests/bittest_pixns
	fi
else
  echo
  echo "    !!!!! MASK SCORER TEST FAILED AT CASE 3 !!!!!    "
  echo
  exit
fi

