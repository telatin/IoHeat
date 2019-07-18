#!/usr/bin/env perl
#  Telegram Bot for IO/Heat
#  Working Draft

use 5.018;
use warnings;
use WWW::Telegram::BotAPI;
use utf8;
use Data::Dumper;
use Term::ANSIColor;
use FindBin qw($RealBin);
use JSON::PP;

our $controller = "$RealBin/ioheat.py";
our %symbol = (
    'ok'       => "\x{2705}",
    'no'       => "\x{1f6ab}",
    'soon'     => "\x{1f51c}",
    'redcross' =>  "\x{274c}",
    'clock'    =>  "\x{1f559}",
    'bug'      => "\x{1f41e}",

    'R'        => "\x{1f422}",
    'Q'        => "\x{1f559}",
    'C'        => "\x{2705}",
    'H'        => "\x{1f6ab}",
);

our $conf;

my ($verbose, $debug, $opt_token) = @ARGV;



# get Telegram API token
unless (defined $opt_token) {
    if ( -e "$ENV{HOME}/.IoHeat.conf" ) {
        $conf = readConfigFromFile("$ENV{HOME}/.IoHeat.conf");
    } elsif (-e "$RealBin/.IoHeat.conf" ) {
        $conf = readConfigFromFile("$RealBin/.IoHeat.conf");
    } else {
        die "APIKey not found. Can be in:\n - $ENV{HOME}/.IoHeat.conf\n - $RealBin/.IoHeat.conf\n - Third parameter [verbose, debug, key]\n";
    }
    $opt_token = $conf->{token};
}

my $api = WWW::Telegram::BotAPI->new (
    token => $opt_token
);

# Bump up the timeout when Mojo::UserAgent is used (LWP::UserAgent uses 180s by default)
$api->agent->can ("inactivity_timeout") and $api->agent->inactivity_timeout (45);
my $me = $api->getMe or die;
my ($offset, $updates) = 0;

# The commands that this bot supports.# file_id of the last sent picture
my $pic_id; 

my $commands = {
    # Example demonstrating the use of parameters in a command.
    "say"      => sub {
            join " ", splice @_, 1 or "Usage: /say something";
    },
    
    
    "whoami"   => sub {
        sprintf "Hello %s, I am %s, your lab technician! How are you?", shift->{from}{username}, $me->{result}{username}
    },
 
    "temp"    => sub {
        my $s = getStatus();
        sprintf "The device is ready.\nCurrent temperature %s degrees.\nStay warm %s!", sprintf("%.1f", $s->{status}->{temperature}), shift->{from}{username};
    },

    "status"    => sub {
      my $s = getStatus();
      my $relay = 'not active';

      $relay = 'heater is active now' if ($s->{status}->{heater_active} eq 'ON');

      my $output = sprintf "Now *%s°C* (hum %s%)\n*Heater is %s* (%s, server: %s %s)",
          sprintf("%.1f", $s->{status}->{temperature}),
          sprintf("%.1f", $s->{status}->{humidity}),
          $s->{status}->{heating_cycle},
          $relay,
          $s->{status}->{process},
          $s->{status}->{elapsed};
      +{
              method     => "sendMessage",
              parse_mode => "Markdown",
              text => $output,
      }
    },

    "start"    => sub {
      print STDERR "[START] Status:\n" if ($debug);
      my $s = getStatus();
      print STDERR Dumper $s if ($debug);
      my $output = '';
      if ($s->{status}->{heating_cycle} eq 'ON') {
        $output .= "Device is _already_ heating. Check with /status\n";
      } else {
        if (ioh_start()) {
          $output .= "*Heating started* at ". sprintf("%.2f", $s->{status}->{temperature})."°C. Check with /status";
        } else {
          $output .= "*ERROR!* I wasn't able to start the heating cycle, and I'm so embarassed about this now. Check with /status"
        }

      }
      +{
              method     => "sendMessage",
              parse_mode => "Markdown",
              text => $output,
      }
    },

    "stop"    => sub {
      my $s = getStatus();
      my $output = '';
      if ($s->{status}->{heating_cycle} eq 'OFF' and $s->{status}->{heater_active} eq 'OFF') {
        $output .= "Heater and heating cycle are _already_ off. Check with /status\n";
      } else {
        if (ioh_stop()) {
          $output .= "*Heating stopped* at ". sprintf("%.2f", $s->{status}->{temperature})."°C. Check with /status";
        } else {
          $output .= "*ERROR!* I wasn't able to stop the heating cycle, and I'm so embarassed about this now. Check with /status"
        }
      }
          +{
                  method     => "sendMessage",
                  parse_mode => "Markdown",
                  text => $output,
          }
        },
    # Example displaying a keyboard with some simple options.
    "keyboard" => sub {
        +{
            text => "Here's your control panel!",
            reply_markup => {
                keyboard => [ [ "/status", "/temp" ], [ "/start", "/stop" ], [ "/whoami", "/lastphoto"] ],
                one_time_keyboard => \1 # \1 maps to "true" when being JSON-ified
            }
        }
    },

    "disk" => sub {
        # DISK FREE
        my $output = simple_disk_free();
        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text => $output,
        }
    },

    # Let me identify yourself by sending your phone number to me.
    "phone" => sub {
        +{
            text => "Would you allow me to get your phone number please?",
            reply_markup => {
                keyboard => [
                    [
                        {
                            text => "Sure!",
                            request_contact => \1
                        },
                        "No, go away!"
                    ]
                ],
                one_time_keyboard => \1
            }
        }
    },
    # Test UTF-8
    "encoding" => sub { "Привет! こんにちは! Buondì!" },
    # Example sending a photo with a known picture ID.
    "lastphoto" => sub {
        return "You didn't send any picture!" unless $pic_id;
        +{
            method  => "sendPhoto",
            photo   => $pic_id,
            caption => "Here it is!"
        }
    },
    "_unknown" => "Unknown command :( Try /help"
};

# Generate the command list dynamically.
$commands->{help} = "Hello, this is your frienly lab technician, Giovanni! Try /" . join " - /", grep !/^_/, keys %$commands;

# Special message type handling
my $message_types = {
    # Save the picture ID to use it in `lastphoto`.
    "photo" => sub { $pic_id = shift->{photo}[0]{file_id} },

    # Receive contacts!
    "contact" => sub {
        my $contact = shift->{contact};
        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => sprintf (
                            "Here's some information about this contact.\n" .
                            "- Name: *%s*\n- Surname: *%s*\n" .
                            "- Phone number: *%s*\n- Telegram UID: *%s*",
                            $contact->{first_name}, $contact->{last_name} || "?",
                            $contact->{phone_number}, $contact->{user_id} || "?"
                        )
        }
    }
};

printf "Hello! I am %s. Starting...\n", $me->{result}{username} if ($verbose);

my $clock_tick = 0;

while (1) {
    if ($verbose and $debug) {
      print STDERR color('bold'), "<$clock_tick> \r";
    }
    $clock_tick++;
    $updates = $api->getUpdates ({
        timeout => 30, # Use long polling
        $offset ? (offset => $offset) : ()
    });


    unless ($updates and ref $updates eq "HASH" and $updates->{ok}) {
        warn "WARNING: getUpdates returned a false value - trying again...";
        next;
    }
    for my $u (@{$updates->{result}}) {
        if ($verbose) {
            print STDERR color('bold green'), "== REQUEST ==", color('reset'),"\n";
            print STDERR color('blue'), Dumper $u;
            print STDERR color('reset'),"\n";
        }

        $offset = $u->{update_id} + 1 if $u->{update_id} >= $offset;
        if (my $text = $u->{message}{text}) { # Text message
            printf "Incoming text message from \@%s\n", $u->{message}{from}{username};
            printf "Text: %s\n", $text;
            if ($text !~ m!^/[^_].!) { # Not a command
                print STDERR color('red'), "Not a command\n", color('reset');
                next;
            }
            my ($cmd, @params) = split / /, $text;
            my $res = $commands->{substr ($cmd, 1)} || $commands->{_unknown};
            # Pass to the subroutine the message object, and the parameters passed to the cmd.
            $res = $res->($u->{message}, @params) if ref $res eq "CODE";
            next unless $res;
            my $method = ref $res && $res->{method} ? delete $res->{method} : "sendMessage";
            $api->$method ({
                chat_id => $u->{message}{chat}{id},
                ref $res ? %$res : ( text => $res )
            });
            print "Reply sent chat_id:",$u->{message}{chat}{id},".\n";
        }
        # Handle other message types.
        for my $type (keys %{$u->{message} || {}}) {
            next unless exists $message_types->{$type} and
                        ref (my $res = $message_types->{$type}->($u->{message}));
            my $method = delete ($res->{method}) || "sendMessage";
            $api->$method ({
                chat_id => $u->{message}{chat}{id},
                %$res
            })
        }
    }
}


sub readConfigFromFile {
    my ($filename) = @_;
    my $conf;
    open my $I, '<', "$filename" || die " FATAL ERROR:\n Unable to open <$filename>\n";
    while (my $l = readline($I) ) {
        if ($l =~/^(\w+)\s*=\s*(.*)$/) {
            $conf->{$1} = $2
        }
    }
    return $conf;
}

sub checkProcess {
  # Check if <ioheat.py> heating is on
  my $cmd = 'ps aux';
  my @out = `$cmd 2>/dev/null`;
  foreach my $line (@out) {
    if ($line=~/ioheat\.py/ and $line=~/-a start/) {
      return 1
    }
  }
  return 0;
}
sub ioh_start {

  if (checkProcess()) {
    debug("\tioh_start(): process already found!");
    return 0;
  }

  system("$controller -j -a start 2>/dev/null &");
  debug("\tioh_start(): heater started!\n") if ($debug);
  if (checkProcess()) {
    debug("\tioh_start(): heater started: SUCCESS (process found)!");
    return 1
  } else {
    deb_warn("\tioh_start(): heater started: PROBLEM HERE (process NOT found)!");
    return 1
  }
}


sub ioh_stop {

  my $cmd = qq($controller -j -a off 2>/dev/null);
  my $data = `$cmd`;
  my $off_error = $?;
  sleep 1;
  if ($off_error) {
    deb_warn("[ioh_stop] \`$cmd\` returned $off_error");
    return 0
  } elsif (! -e "$ENV{HOME}/.IoHeat.lock") {
    return 1
  } else {
      deb_warn("[ioh_stop] lock file found (?)");
      return 1
  }

}

sub lockfile_age {
  my $file = "$ENV{HOME}/.IoHeat.lock";
  my $secs = time - (stat($file))[9];
  return formatsec($secs);
}


sub formatsec {
 my $time = shift;
 my $days = int($time / 86400);
  $time -= ($days * 86400);
 my $hours = int($time / 3600);
  $time -= ($hours * 3600);
 my $minutes = int($time / 60);
 my $seconds = $time % 60;

 $days = $days < 1 ? '' : $days .'d ';
 $hours = $hours < 1 ? '' : $hours .'h ';
 $minutes = $minutes < 1 ? '' : $minutes . 'm ';
 $time = $days . $hours . $minutes . $seconds . 's';
 return $time;
}

sub getStatus {

  my $cmd = qq($controller -j -a status 2>/dev/null);
  my $json = `$cmd`;
  my $status = decode_json $json;

  if (checkProcess()) {
    $status->{status}->{process} = 'ON';
    $status->{status}->{elapsed} = lockfile_age();
  } else {
    $status->{status}->{process} = 'OFF';
    $status->{status}->{elapsed} = '';
  }
  return $status;
}

sub getTempHist {
    return undef;
}

sub getTemperature {
    my $output = `temperature`;
    my ($temp) = split /,/, $output;
    return $temp;
}
sub simple_disk_free {
    my $nice_output = '';
    my @lines = `df | grep dev.[sdv]`;
    foreach my $line (@lines) {
        my ($volume, $size, $used, $avail) = split /\s+/, $line;
        next unless ($size);
        verbose(" [DISK] $volume $used/$size (avail: $avail)\n");
        my $ratio = sprintf("%.1f", 100 * $used/$size);
        my $free = sprintf("%.1f", $avail / (1000 * 1000) ) . 'Gb';
        $nice_output .= "*$volume* ($ratio\% full): $free free\n";
    }

    return $nice_output || 'Nothing to show';
}


sub verbose {
  return undef if (not $verbose);
  print STDERR color('cyan'), '> ', color('reset'), $_[0], "\n";

}
sub debug {
  return undef if (not $debug);
  print STDERR color('yellow'), $_[0], color('reset');
}
sub deb_warn {
  return undef if (not $debug);
  print STDERR color('red'), $_[0], color('reset'),"\n";

}
__END__

