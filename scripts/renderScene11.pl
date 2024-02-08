#!/usr/bin/perl -w
use File::Basename;
use Cwd 'abs_path';

my $scriptDir = abs_path(dirname(__FILE__));
my $tag = shift @ARGV;
$tag or die "NEED SIM TAG";
my $srcpath = "$scriptDir/../data/$tag/imgs";
my $destpath = "$scriptDir/../data/merges/$tag.mp4";

my $ffmpeg = "/data/ackley/AV/FUJIFILM-X-T4/scripts/ffmpeg-git-20220108-amd64-static/ffmpeg";

my ($finalwidth,$finalheight) = (1920,1080);
my $fontsize=28;
my $fontcolor='DarkGray';
my $fontgap=8;
#stampwidth@32: 208 -> hhh:mm:ss.9
#stampwidth@28: 186 -> hhh:mm:ss.9
#stampwidth@28: 158 -> hhh:mm:ss
my $stampwidth = 158;
my $timestampcrop=$finalwidth-$stampwidth-$fontgap;
my $fontfile="/data/ackley/AV/FUJIFILM-X-T4/scripts/fonts/NotoMono-Regular.ttf";

print("$srcpath -> $destpath\n");
#ffmpeg -f image2 -r 60 -i step%08d.png -vcodec libx264 -vf 'pad=1920:1080:(ow-iw)/2:(oh-ih)/2:0x0f0f0f' -r 60 -pix_fmt yuv420p ../../merges/20240123-075310.mp4

#my $init = "-f image2 -r 60";
my $init = "";
my $persrc = "-pattern_type glob -f image2 -framerate 60";
my $src0 = "$persrc -i '$srcpath/view/*.png'"; 
my $src1 = "$persrc -i '$srcpath/SLFL/*.png'";
my $src2 = "$persrc -i '$srcpath/SRFL/*.png'";
my $src3 = "$persrc -i '$srcpath/SUPL/*.png'";
my @srcs = ($src0,$src1,$src2,$src3);
my $dest = "-r 60 $destpath";
my $eyesc = 1.5;
my @filters;
push @filters, "[0]split=2[s1][s2]";
push @filters, "[1]scale=$eyesc*iw:$eyesc*ih[lscale]";
push @filters, "[2]scale=$eyesc*iw:$eyesc*ih[rscale]";
push @filters, "[3]scale=$eyesc*iw:$eyesc*ih[uscale]";
push @filters, "[lscale]pad=width=iw+4:height=ih+4:x=2:y=2:color=black[left]";
push @filters, "[rscale]pad=width=iw+4:height=ih+4:x=2:y=2:color=black[right]";
push @filters, "[uscale]pad=width=iw+4:height=ih+4:x=2:y=2:color=black[up]";
push @filters, "[left][up][right]hstack=inputs=3[eyes]";
push @filters, "[s1][eyes]overlay=x=(main_w-overlay_w)/2:y=8[main]";
push @filters, "[s2]drawtext=fontfile='$fontfile':fontcolor=$fontcolor:fontsize=$fontsize:x=$fontgap:y=$fontgap:text=%{pts\\\\:hms}[fulltimestamp]";
push @filters, "[fulltimestamp]crop=w=iw-$timestampcrop:h=ih:x=0:y=0[timestamp]";
push @filters, "[main][timestamp]overlay=x=0:y=0[out]";
my $complex_filter = join(";",@filters);
my $cmd = "$ffmpeg -y @srcs -filter_complex '$complex_filter' -map '[out]' $dest";
print("$cmd\n");
system($cmd);
print("FINISHED RENDERING $tag\n");
exit;
# /data/ackley/AV/FUJIFILM-X-T4/scripts/ffmpeg-git-20220108-amd64-static/ffmpeg  -pattern_type glob  -f image2 -framerate 60 -i '/data/ackley/PART4/code/D/PyBulletTime/data/20240123-075310/imgs/viewl*.png' -pattern_type glob  -f image2 -framerate 60 -i '/data/ackley/PART4/code/D/PyBulletTime/data/20240123-075310/imgs/viewr*.png' -filter_complex hstack=inputs=2 -r 60 /data/ackley/PART4/code/D/PyBulletTime/data/merges/20240123-075310x.mp4
