#!/usr/bin/env perl
use FindBin qw($RealBin);
use 5.012;
my ($text, $when) = @ARGV;
die "Usage: text when \n" unless ($when);
my $date = `date +"%Y%m%d_%H.%M"`;
chomp($date);

my $cmd = "at $when date >> $RealBin/req_$date.log";
say $cmd;
system($cmd);
