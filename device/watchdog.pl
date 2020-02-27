#!/usr/bin/env perl 
use 5.018;
use warnings;
my $bot = '/home/pi/Desktop/ioheat/giovanni_bot.pl';
my $proc_count = 0;
my @proc = `ps a`;
foreach my $p (@proc) {
 if ($p =~/giovanni_bot.pl/) {
  $proc_count++;
 }
}

if ($proc_count == 0) {
  print "Restarting Giovanni [/tmp/bot.*]\n";
  exec("perl $bot > /tmp/bot.out 2> /tmp/bot.log &");
} else {
  print "Giovanni is alive!\n";
}
