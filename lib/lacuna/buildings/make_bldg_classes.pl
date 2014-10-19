
use v5.14;
use Data::Dumper;
use File::Slurp;
use JSON;

my $json = read_file 'resources.json';
my $hr = decode_json $json;

open my $init, '>>', '__init__.py' or die;
foreach my $bldg_name( sort keys %{$hr->{'buildings'}} ) {
    $bldg_name =~ s{^/}{};

    say $init "from lacuna.buildings.$bldg_name import $bldg_name"

    my $fn = $bldg_name . '.py';
    unless( -e $fn ) {
        open my $f, '>', $fn or die;
        print $f make_class($bldg_name);
        close $f;
    }
}
close init;

sub make_class {
    my $class = shift;

    return "
from lacuna.building import Building

class $class(Building):
    path = '$class'

    def __init__( self, client, body_id:int = 0, building_id:int = 0 ):
        super().__init__( client, body_id, building_id )
";

}
