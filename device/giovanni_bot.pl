#!/usr/bin/env perl
#  Telegram Bot for IO/Heat
#  Working Draft

use 5.018;
use utf8;
use open qw( :encoding(UTF-8) :std );
use FindBin qw($RealBin);
use WWW::Telegram::BotAPI;

use Data::Dumper;
use Term::ANSIColor;

use JSON::PP;

our $controller = "$RealBin/ioheat.py";
my $test_logo_path = "/Users/telatin/git/hub/ioheat/misc/logo_small_0.png";
our %emoji = (
    'bot'      => '🤖',
    'temp'     => '🌡',
    'clock'    => '🕙',
    'fire'     => '🔥',
    'loop'     => '🔄',
    'ok'       => "✅",     # green heavy check mark
    'no'       => "🚫",     #  U+1F6AB NO ENTRY SIGN
    'redcross' => "❌",     #  U+274C CROSS MARK
    'warning'  => '⚠️',
    'bug'      => "🐞",     #  U+1F41E LADY BEETL
    'soon'     => "🔜",     #  Soon right arrow
    'turtle'   => "🐢",     #  U+1F422 TURTLE
    'alarm'    => "⏰",     #  alarm clock
    'smile'    => "😃",     #  smile
    'cool'     => '😎',
    'sleep'    => '😴',

);

our $conf;

my ( $verbose, $debug, $opt_token ) = @ARGV;


# get Telegram API token
unless ( defined $opt_token ) {
    if ( -e "$ENV{HOME}/.IoHeat.conf" ) {
        $conf = readConfigFromFile("$ENV{HOME}/.IoHeat.conf");
    }
    elsif ( -e "$RealBin/.IoHeat.conf" ) {
        $conf = readConfigFromFile("$RealBin/.IoHeat.conf");
    }
    else {
        die "APIKey file not found. Can be in:\n - $ENV{HOME}/.IoHeat.conf\n - $RealBin/.IoHeat.conf\n - Third parameter [verbose, debug, key]\n";
    }
    $opt_token = $conf->{token};
}

my $api = WWW::Telegram::BotAPI->new( token => $opt_token );

# Bump up the timeout when Mojo::UserAgent is used (LWP::UserAgent uses 180s by default)
$api->agent->can("inactivity_timeout") and $api->agent->inactivity_timeout(45);
my $me = $api->getMe or die;
my ( $offset, $updates ) = 0;

# The commands that this bot supports.# file_id of the last sent picture
my $pic_id;

my $commands = {

    # Example demonstrating the use of parameters in a command.
    "say" => sub {
        if ( defined $_[1] ) {
            push( @_, $emoji{'smile'} );
            join " ", splice @_, 1;
        }
        else {
            "Usage: /say something";
        }

    },
    "update" => sub {
	my $raw = `$RealBin/update 2>&1`;
        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => $raw,
        };

    },
    "hello" => sub {

        my $u = '' . $me->{result}{username};
        
        my $message = "Hello "
          . shift->{from}{username}
          . ",\n I am $emoji{bot} *IoHeat Bot* [\@$u], your lab technician! How are you?";

        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => $message,
        };
    },

    "temp" => sub {
        my $s = getStatus();

        #sprintf "The device is ready.\n $emoji{temp} %s degrees.\nStay warm %s!", sprintf("%.1f", $s->{status}->{temperature}), shift->{from}{username};
        print "The device is ready.\n $emoji{temp} %s degrees.\nStay warm %s!",
          sprintf( "%.1f", $s->{status}->{temperature} ),
          shift->{from}{username};
    },

    "status" => sub {
        my $s     = getStatus();
        my $relay = "$emoji{sleep} not active";

        $relay = "$emoji{loop} heater is active now"
          if ( $s->{status}->{heater_active} eq 'ON' );

        my $output =
          sprintf "$emoji{temp} *%s°C* (hum %s%)\n*Heater is %s* (%s, server: %s %s)",
          sprintf( "%.1f", $s->{status}->{temperature} ),
          sprintf( "%.1f", $s->{status}->{humidity} ),
          $s->{status}->{heating_cycle},
          $relay,
          $s->{status}->{process},
          $s->{status}->{elapsed};

        $output .= "\n" . ioh_queue();
        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => $output,
        };
    },

    "start" => sub {
        print STDERR "[START] Status:\n" if ($debug);
        my $s = getStatus();
        print STDERR Dumper $s if ($debug);
        my $output = '';
        if ( $s->{status}->{heating_cycle} eq 'ON' ) {
            $output .= "$emoji{warning} Device is _already_ heating. Check with /status\n";
        }
        else {
            if ( ioh_start() ) {
                $output .=  "$emoji{fire} *Heating started* at "
                  . sprintf( "%.2f", $s->{status}->{temperature} )
                  . "°C. Check with /status";
            }
            else {
                $output .= "$emoji{redcross} *ERROR!* I wasn't able to start the heating cycle, and I'm so embarassed about this now. Check with /status";
            }

        }


        if ( defined $_[1] ) {
            shift @_;
            $output .= "\n\n$emoji{warning} No parameters were expected: @_ ignored";
        }
        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => $output,
        };
    },

    "schedule" => sub {
        print STDERR "[schedule] Status:\n" if ($debug);
        my $s = getStatus();
        print STDERR Dumper $s if ($debug);
        shift(@_);
         
        my $output = "$emoji{warning} Tell me when like:\n • now + 2 minutes\n • now + 10 hours\n • 10am tomorrow";
        if ( defined $_[0] ) {
            my $time = join " ", @_;
            $output = ioh_schedule($time);
        }

        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => $output,
        };
    },

    "queue" => sub {
        my $s = getStatus();
        print STDERR Dumper $s if ($debug);
        my ( $output, $count ) = ioh_queue();

        if ( defined $_[1] ) {
            shift @_;
            $output .= "\n\n$emoji{warning} No parameters were expected: @_ ignored";
        }

        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => "$emoji{clock} $output",
        };
    },
    "delete" => sub {
        shift(@_);
        my $output = ioh_queue_delete($_[0]);

        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => "$output",
        };
    },
    "stop" => sub {
        my $s      = getStatus();
        my $output = '';
        if (    $s->{status}->{heating_cycle} eq 'OFF'
            and $s->{status}->{heater_active} eq 'OFF' )
        {
            $output .= "$emoji{warning} Heater and heating cycle are _already_ off. Check with /status\n";
        }
        else {
            if ( ioh_stop() ) {
                $output .= "$emoji{ok} *Heating stopped* at "
                  . sprintf( "%.2f", $s->{status}->{temperature} )
                  . "°C. Check with /status";
            }
            else {
                $output .= "$emoji{warning} *ERROR!* I wasn't able to stop the heating cycle, and I'm so embarassed about this now. Check with /status";
            }
        }

        if ( defined $_[1] ) {
            shift @_;
            $output .= "\n\n$emoji{warning} No parameters were expected: @_ ignored";
        }
        +{
            method     => "sendMessage",
            parse_mode => "Markdown",
            text       => $output,
        };
    },

    # Example displaying a keyboard with some simple options.
    "keyboard" => sub {
        +{
            text         => "$emoji{smile} Here's your control panel!",
            reply_markup => {
                keyboard => [
                    [ "/status", "/temp" ],
                    [ "/start",  "/stop" ],
                    [ "/queue",  "/schedule" ]
                ],
                one_time_keyboard =>
                  \1    # \1 maps to "true" when being JSON-ified
            }
        };
    },

    # Let me identify yourself by sending your phone number to me.
    "phone" => sub {
        +{
            text => "$emoji{warning} This is a test\nWould you allow me to get your phone number please?",
            reply_markup => {
                keyboard => [
                    [
                        {
                            text            => "Sure!",
                            request_contact => \1
                        },
                        "No, go away!"
                    ]
                ],
                one_time_keyboard => \1
            }
        };
    },

    # Test UTF-8
    "encoding" => sub {
        "$emoji{smile} Hello test! Привет! こんにちは! Buondì!";
    },

    "logo" => sub {
        return 'Meh...' if ( not -e "$test_logo_path" );
        +{
            method => "sendPhoto",
            photo  => {
                file => $test_logo_path
            },
            caption => "Here it is!"
          }

    },



    # Example sending a photo with a known picture ID.
    "lastphoto" => sub {
        return "You didn't send any picture!" unless $pic_id;
        +{
            method  => "sendPhoto",
            photo   => $pic_id,
            caption => "Here it is!"
        };
    },
    "_unknown" => "Unknown command :( Try /help"
};

# Generate the command list dynamically.
$commands->{help} =
  "Hello, this is your frienly lab technician, Giovanni! Try /" . join " - /",
  grep !/^_/, keys %$commands;

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
            text       => sprintf(
                "Here's some information about this contact.\n"
                  . "- Name: *%s*\n- Surname: *%s*\n"
                  . "- Phone number: *%s*\n- Telegram UID: *%s*",
                $contact->{first_name},   $contact->{last_name} || "?",
                $contact->{phone_number}, $contact->{user_id}   || "?"
            )
        };
    }
};

verbose("Hello! I am $emoji{bot} ". $me->{result}{username} . ". Starting..." );
deb("Debug=$debug;Verbose=$verbose;");
my $clock_tick = 0;

while (1) {
    if ( $verbose and $debug ) {
        print STDERR color('bold'), "<$clock_tick> \r";
    }
    $clock_tick++;
    $updates = $api->getUpdates(
        {
            timeout => 30,    # Use long polling
            $offset ? ( offset => $offset ) : ()
        }
    );

    unless ( $updates and ref $updates eq "HASH" and $updates->{ok} ) {
        warn "WARNING: getUpdates returned a false value - trying again...";
        next;
    }
    for my $u ( @{ $updates->{result} } ) {


        if ($verbose) {
            print STDERR color('bold magenta'), "== REQUEST ==", color('reset'),
              "\n";
            print STDERR color('magenta'),  Dumper $u;
            print STDERR color('reset'), "\n";
        }

        $offset = $u->{update_id} + 1 if $u->{update_id} >= $offset;

        if ( my $text = $u->{message}{text} ) {    
            # Text message (i.e. not a photo / sticker)

            printf "START. Incoming text message from \@%s\n",    $u->{message}{from}{username};
            printf "       Text: %s\n", $text;

            if ( $text !~ m!^/[^_].! ) {

                # Not a command
                print STDERR color('red'), "Not a command\n", color('reset');
                next;
            }

            my ( $cmd, @params ) = split / /, $text;
            
            deb(qq(cmd="$cmd"));
            deb("params=".join(',', @params));
            my $res = $commands->{ substr( $cmd, 1 ) } || $commands->{_unknown};
            deb("ref=" . ref $res);

            # Pass to the subroutine the message object, and the parameters passed to the cmd.
            # ref $res == CODE --> valid command
            $res = $res->( $u->{message}, @params ) if ref $res eq "CODE";


            say STDERR color('blue'), Dumper $res;
            say STDERR color('reset');
            next unless $res;


            my $method = ref $res
              && $res->{method} ? delete $res->{method} : "sendMessage";
            $api->$method(
                {
                    chat_id => $u->{message}{chat}{id},
                    ref $res ? %$res : ( text => $res )
                }
            );
            print "END.   Reply sent chat_id:", $u->{message}{chat}{id}, ".\n";
        }

        # Handle other message types.
        for my $type ( keys %{ $u->{message} || {} } ) {
            next
              unless exists $message_types->{$type}
              and ref( my $res = $message_types->{$type}->( $u->{message} ) );
            my $method = delete( $res->{method} ) || "sendMessage";
            $api->$method(
                {
                    chat_id => $u->{message}{chat}{id},
                    %$res
                }
            );
        }
    }
}

sub readConfigFromFile {
    my ($filename) = @_;
    my $conf;
    open my $I, '<',
      "$filename" || die " FATAL ERROR:\n Unable to open <$filename>\n";
    while ( my $l = readline($I) ) {
        if ( $l =~ /^(\w+)\s*=\s*(.*)$/ ) {
            $conf->{$1} = $2;
        }
    }
    return $conf;
}

sub checkProcess {

    # Check if <ioheat.py> heating is on
    my $cmd = 'ps aux';
    my @out = `$cmd 2>/dev/null`;
    foreach my $line (@out) {
        if ( $line =~ /ioheat\.py/ and $line =~ /-a start/ ) {
            return 1;
        }
    }
    return 0;
}

sub ioh_queue_delete {
     my $id = shift @_;
     if ($id < 1) {
        return "$emoji{warning} Specify a schedule ID (use /queue to get IDs)";
     }
     if (queue_clear($id)) {
        return "$emoji{ok} Task *$id* has been deleted (check with /queue)";
     } else {
        return "$emoji{warning} Some problems trying to delete task *$id* (check with /queue)";
     }
}
sub queue_clear {
    my $id = shift @_;
    return 0 unless $id;
    my $cmd = `atrm $id`;
    if ($?) {
        return 0;
    } else {
        return 1;
    }

}
sub ioh_queue {
    my $cmd = qq(atq);
    my $out = '';
    my @out = `$cmd`;
    my $c   = 0;
    foreach my $l (@out) {
        chomp($l);
        $c++;
        $l =~s/^(\d{1,3})\s*(\w{3})\s+(\w{3}\s+\d{1,2})/*#\1* • \2 _\3_/;
        $l =~s/(\d{2}:\d{2}):\d{2}/\1/;
        $out .= "$l\n";
    }
    $out = "_$c requests scheduled_\n" . $out;
    print STDERR "ioh_queue(): c=$c\n";
    print STDERR "ioh_queue(): m=$c\n";
    return ( $out, $c );
}

sub ioh_schedule {
    my $when    = shift(@_);
    my $message = '';
    $when = 'now' if ( !$when );
    my $cmd = qq(echo '$controller -j -a start 2>/dev/null' | at $when 2>&1);
    print STDERR "ioh_schedule(): $cmd\n";

    
    my $schedule = `$cmd`;

    my ( $queue, $total ) = ioh_queue();

    if ($?) {
        $message .= "$emoji{no} _bad time format_\n";
    }
    else {
        $message .= "$emoji{ok} Your request was queued.\nThere are *$total* requests (see /queue) ";
    }
}

sub ioh_start {

    if ( checkProcess() ) {
        deb("\tioh_start(): process already found!");
        return 0;
    }

    system("$controller -j -a start 2>/dev/null &");
    deb("\tioh_start(): heater started!\n") if ($debug);
    if ( checkProcess() ) {
        deb("\tioh_start(): heater started: SUCCESS (process found)!");
        return 1;
    }
    else {
        deb_warn(
            "\tioh_start(): heater started: PROBLEM HERE (process NOT found)!");
        return 1;
    }
}

sub ioh_stop {

    my $cmd       = qq($controller -j -a off 2>/dev/null);
    my $data      = `$cmd`;
    my $off_error = $?;
    sleep 1;
    if ($off_error) {
        deb_warn("[ioh_stop] \`$cmd\` returned $off_error");
        return 0;
    }
    elsif ( !-e "$ENV{HOME}/.IoHeat.lock" ) {
        return 1;
    }
    else {
        deb_warn("[ioh_stop] lock file found (?)");
        return 1;
    }

}

sub lockfile_age {
    my $file = "$ENV{HOME}/.IoHeat.lock";
    if ( -e $file ) {
        my $created = ( stat($file) )[9];
        my $secs    = time - $created;
        return formatsec($secs);
    }
    else {
        return '';
    }
}

sub formatsec {
    my $time = shift;
    my $days = int( $time / 86400 );
    $time -= ( $days * 86400 );
    my $hours = int( $time / 3600 );
    $time -= ( $hours * 3600 );
    my $minutes = int( $time / 60 );
    my $seconds = $time % 60;

    $days    = $days < 1    ? '' : $days . 'd ';
    $hours   = $hours < 1   ? '' : $hours . 'h ';
    $minutes = $minutes < 1 ? '' : $minutes . 'm ';
    $time = $days . $hours . $minutes . $seconds . 's';
    return $time;
}

sub getStatus {

    my $cmd  = qq($controller -j -a status 2>/dev/null);
    my $json = `$cmd`;
    if ($?) {
        return undef;
    }
    my $status = decode_json $json;
    my ( undef, $jobs ) = ioh_queue();
    $status->{status}->{jobs} = $jobs;
    if ( checkProcess() ) {
        $status->{status}->{process} = 'ON';
        $status->{status}->{elapsed} = lockfile_age();
    }
    else {
        $status->{status}->{process} = 'OFF';
        $status->{status}->{elapsed} = '';
    }
    return $status;
}

sub getTempHist {
    return undef;
}

 

sub simple_disk_free {
    my $nice_output = '';
    my @lines       = `df | grep dev.[sdv]`;
    foreach my $line (@lines) {
        my ( $volume, $size, $used, $avail ) = split /\s+/, $line;
        next unless ($size);
        verbose(" [DISK] $volume $used/$size (avail: $avail)\n");
        my $ratio = sprintf( "%.1f", 100 * $used / $size );
        my $free = sprintf( "%.1f", $avail / ( 1000 * 1000 ) ) . 'Gb';
        $nice_output .= "*$volume* ($ratio\% full): $free free\n";
    }

    return $nice_output || 'Nothing to show';
}

sub verbose {
    return undef if ( not $verbose );
    print STDERR color('cyan'), '[#] ', color('reset'), $_[0], "\n";

}

sub deb {
    return undef if ( not $debug );
    print STDERR color('yellow'), '[~] ', color('reset'), $_[0], "\n";
    return 0;
    
}

sub deb_warn {
    return undef if ( not defined $debug );
    print STDERR $emoji{warning}, '   ', color('yellow'), $_[0], color('reset'), "\n";

}
__END__
