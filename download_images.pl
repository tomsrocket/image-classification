

#!/usr/bin/perl

use warnings;
use strict;

use LWP::Simple;
use HTML::LinkExtor;
use Data::Dumper;
$Data::Dumper::Indent=1;

die "usage: $0 [http://url] [target_directory]\n" if @ARGV != 2;
my $url = shift;
my $dir = shift;
$|++;

if ( $url !~ /^http/ ) { 
  print "usage: url ( http(s)://www.example.com/ directory )\n"; 
  exit(1);
}

my %images = (); 
my $html = get($url) 
  or die "could not get $url\n";

my $parser = HTML::LinkExtor->new(undef, $url);
$parser->parse($html);

my @all_link_refs = $parser->links();

for my $link_ref ( @all_link_refs  ) { 
  my ( $html_tag, $attr_name, $this_url ) = @$link_ref;
  if ( ($html_tag eq 'img') ) { 
    my $image_name = (split("/", $this_url))[-1];
    $images{$image_name}++;

    if ( $images{$image_name} == 1  ) { 
        print "Downloading $this_url to $image_name...\n";
        open my $PIC, ">", "$dir/$image_name";
        my $image = get($this_url);
        print $PIC $image;
    }   
  }
}