
use v5.14;
use warnings;
use File::Copy;
use File::Find;
use File::Slurp;
use File::Temp;

File::Copy::mv( '_build/html/_static',  '_build/html/static'  );
File::Copy::mv( '_build/html/_modules', '_build/html/modules' );

my $files_fixed = 0;
find( \&wanted, '_build/html' );

say "I just fixed $files_fixed files.";


sub wanted {
    ### $File::Find::dir - current dir
    ### $File::Find::name - full pathname to file
    ### $_ - current filename
 
    return unless $_ =~ /\.html$/;

    my $tmp_fh = File::Temp->new( UNLINK => 0 );
    my $tmp_fn = $tmp_fh->filename;
    close $tmp_fh;

    my $input = File::Slurp::read_file( $_ );
    $input =~ s/_static/static/g;
    $input =~ s/_modules/modules/g;
    File::Slurp::write_file( $tmp_fn, $input );

    File::Copy::mv( $tmp_fn, $_) or die $!;
    unlink $tmp_fn;
    $files_fixed++;
}

