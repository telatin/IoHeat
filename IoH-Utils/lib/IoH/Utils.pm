use 5.018;
use warnings;
use Term::ANSIColor;
package IoH::Utils;
#ABSTRACT: Helper subroutines for the 'IoHeat' device prototype (laboratory medium heater, controlled via Internet, using a RaspberryPi3)

$IoH::Utils::VERSION = '0.1';
$IoH::Utils::AUTHOR = 'Andrea Telatin';


=head2 new()

Initialize object properties:
  - verbose
	- test

=cut

sub new {
    my ($class, $args) = @_;
    my $self = {
        verbose  => $args->{verbose},
				test     => $args->{test},
				apiurl   => $args->{apiurl} // 'https://seq.space/apps/ioheat/api/',
				nocolor  => $args->{nocolor} // $ENV{NOCOLOR},
    };
    my $object = bless $self, $class;


    return $object;
}


=head2 check_device()

A subroutine invoked to ensure the library is installed in a "IoHeat" device,
I<i. e.> in a Raspberry Pi running Raspbian and with the temperature sensor and
controlling relais installed.

=cut

sub check_device {

}

sub get_uuid {
	if (defined getvar('test')) {
		return '0000-0000-0000';
	}
	my $uuid = `cat /proc/cpuinfo 2>/dev/null| grep Serial | cut -d ' ' -f 2 `;
	if ($? == 0) {
		chomp($uuid);
		return $uuid;
	} else {
		return undef;
	}
}

=head2 getvar('var_name')

Returns the value of a I<device variable>, that is checked primarily as object property
and as lower-priority as shell environment variable. Returns C<unset> if not found.

=cut

sub getvar {
	my ($self, $var) = @_;
	if (defined $self->{$var}) {
			return $self->{$var};
	} elsif (defined $ENV{"IoH_$var"}) {
		return $ENV{"IoH_$var"};
	}
}


=head2 is_device()

check that the computer running the script looks like a IoHeat device
=cut

sub is_device() {
	my ($self) = @_;

}
1;
