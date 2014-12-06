

#!/usr/bin/perl

use warnings;
use strict;

use LWP::Simple;
use HTML::LinkExtor;
use Data::Dumper;
$Data::Dumper::Indent=1;

die "usage: $0 [filename] [directory] [start_row]\n" if @ARGV != 3;
my $filename = shift;
my $dir = shift;
my $start_row = shift || 0;
$|++;

my %images = (); 

use strict;
use warnings;

open my $info, $filename or die "Could not open $filename: $!";

my $linenr = 0; 
while( my $line = <$info>)  {   
    next unless ( ++$linenr > $start_row );
    if ( $line =~ /^[^,]+,[^,]+,([^,]+jpg)/ ) {
        my $file = $1;
        my $url = 'https://s3-us-west-1.amazonaws.com/logo-crowdsourcing/logo-images/'. $file;
        print "$linenr Downloading $file..\n";
        getstore( $url, "$dir/$file" );
    }

}
