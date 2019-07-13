#!/usr/bin/env perl

use 5.012;
use warnings;
use LWP::Simple;
use Getopt::Long;
use FindBin qw($Bin);
use lib "$Bin/../IoH-Utils/lib/";
use IoH::Utils;

my $opt_test;
my $opt_verbose;
my $opt_nocolor;
my $opt_apiurl;

my $_opt = GetOptions(
	't|test'    => \$opt_test,
	'v|verbose' => \$opt_verbose,
	'no-color'  => \$opt_nocolor,
	'a|apiurl'  => \$opt_apiurl,
);


my $IOH = IoH::Utils->new({
	verbose  => $opt_verbose,
	test     => $opt_test,
	nocolor  => $opt_nocolor,
	apiurl   => $opt_apiurl,
});

print "IoH_test: ", $IOH->getvar('test');
exit;

if (my $uuid = get_rpi_uuid()) {
   my $answer = get($IOH->{'apiurl'}."register.php?device=$uuid");
} else {
	die " FATAL ERROR:\n RaspberryPi UUID not found. Is this Linux? Is this a RaspberryPi?\n";
}
