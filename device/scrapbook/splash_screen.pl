#!/usr/bin/env perl
use 5.012;
use Term::ANSIColor qw(:constants color);
use Term::ReadKey;
my ($wchar, $hchar, $wpixels, $hpixels) = GetTerminalSize();

my $padding = 4;
my $pad = ' ' x $padding;

my $w = $wchar - (2 * $padding);

my $title_string = ' ** IoHeat ** ';
my $title_sub    = ' v 0.1 ';

my $title = color('bold white on_red') . $title_string . color('yellow on_red'). $title_sub;
my $spacer = color('bold white on_red') . ' ' x (($w - length($title_string) - length($title_sub)) / 2);
say '';
say $pad, color('bold white on_red'), ' ' x $w, RESET;
say $pad, $spacer, $title,$spacer, RESET ;
say $pad, color('bold white on_red'), ' ' x $w, RESET;
say '';

