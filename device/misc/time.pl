#!/usr/bin/perl
use warnings;
use strict;
use feature qw{ say };

use Time::ParseDate;
use Time::Piece;

my $string = '11:50:45.242 EDT OCT 27 2015';
my $sec = parsedate($string);
my $tp = do {
    local $ENV{TZ} = 'UTC';
    localtime $sec
};
my ($microsec) = $string =~ /\.([0-9]+)/;  # Microseconds not handled 
say $tp->strftime("%Y-%m-%d %H:%M:%S.$microsec");
