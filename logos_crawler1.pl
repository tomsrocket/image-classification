#!/usr/bin/perl


use LWP::Simple;
use Log;
use HTML::Strip;
use File::Type;

my $ft = File::Type->new();

my $start = $ARGV[0] || 4300;

log_debug("moin");


sub fetch_html {
	my $url = shift;
	my $content = get( $url ); 
	if (defined $content) {
		return $content;
	} else {
		log_error( "HTML fetch error on ", $url );
	}
}

sub find_addresses {
	my $html = shift;
	my $hs         = HTML::Strip->new();
	my $clean_text = $hs->parse( $html );
	$hs->eof;

	my $address = {};

	my $matches = {
		name 	=> 'Name:\s*\n\s*(.+)\n',
		address => 'Strasse:\s*\n\s*(.+)\n',
		city 	=> 'Ort:\s*\n\s*(.+)\n'
	};
	my $raw_matches = {
		phone => '<p\s+class="telefon">([^<]+)<\/p>',
		www   => '<a\s+class="schrift20\s+keinstrich"\s+href="([^"]+)"',
		logo  => '<img\s+src="([^"]+)"\s+alt="Firmenbanner"'
	};
	
	#log_debug("clean_text", $clean_text );
	for my $key (keys %$matches ) {
		my $match = $matches->{$key};
		if ( $clean_text =~ /$match/ ) {
			$address->{$key} = $1;
			log_debug("found $key:", $1 );
		} else {
			log_error( 'did not find', $key )
		}
	}
	for my $key (keys %$raw_matches ) {
		my $match = $raw_matches->{$key};
		if ( $html =~ /$match/ims ) {
			$address->{$key} = $1;
			log_debug("found $key:", $1 );
		} else {
			log_error( 'did not find', $key )
		}
	}
	return $address;
}

sub c {
	my $string = shift;
	$string =~ s/\t/\s/g;
	return $string;
}

sub main {
	for ( $i= $start;$i<100000;$i++ ) {
		my $url = 'http://branchenknecht.de/Firma/' . $i ;
		log_info("==========> processing", $url );
		my $html = fetch_html( $url );
		my $address = find_addresses( $html );
		if ( $address->{logo} ) {
			$address->{logo} =~ s/^..\//http:\/\/branchenknecht.de\//;
			my ($content_type) = head $address->{logo};
			my $suffix = '';
			$suffix = '.jpg' if $content_type eq 'image/jpeg';
			unless ( $suffix ) {
				log_error( "Unknown content type" , $content_type ) ;
				die();
			}
			my $filename = 'logos/logo'.$i.$suffix;
			getstore( $address->{logo}, $filename );
			my $type_from_file = $ft->checktype_filename( $filename );
			my $suffix = '';
			if ($type_from_file ne 'image/jpeg') {
				log_debug("logo type is: $type_from_file"),

				my $new_filename = $filename;
				$new_filename =~ s/.jpg$/.png/i if ( $type_from_file eq 'image/x-png' );
				$new_filename =~ s/.jpg$/.bmp/i if ( $type_from_file eq 'image/x-bmp' );
				$new_filename =~ s/.jpg$/.gif/i if ( $type_from_file eq 'image/gif' );

				if ( $new_filename ne $filename ) {
					rename $filename, $new_filename;
				} else {
					die();
				}

			}


		}

		log_debug( $address );
		next unless ($address->{name} || $address->{address});
		open FILE, ">>addresses.tsv" or die $!;
		print FILE c($address->{name})."\t".c($address->{address}).",".c($address->{city})."\t".c($address->{phone})."\t".c($address->{www})."\t".$i."\t".$address->{logo}."\n";
		close FILE;



	}
}

main();