#!/usr/bin/perl -w
use File::Basename;
use Cwd 'abs_path';

my $scriptDir = abs_path(dirname(__FILE__));
my $tag = shift @ARGV;
$tag and die "NO ARGS ALLOWED";
my $datapath = "$scriptDir/../data";

opendir(H,$datapath) or die $!;
my @datadirs = sort { $b cmp $a} grep { /^\d+-\d+$/ } readdir(H); 
closedir(H) or die $!;

scalar(@datadirs) or die "No data dirs in $datapath";
my $newest = shift @datadirs;
print("RENDERING $newest\n");
exec("$scriptDir/renderScene.pl", $newest);

