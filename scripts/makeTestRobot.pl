#!/usr/bin/perl -w

my $pi = 3.1415926;
my $pio2 = $pi/2;
my ($wheellen,$wheelrad) = (0.02, 0.046);
my ($asym) = (0.000);
my ($lwheelrad,$rwheelrad) = ($wheelrad-$asym,$wheelrad+$asym);

# DON'T FUCK CASUALLY WITH THE FOLLOWING FRICTION NUMBERS!
my ($wheellateralfric,$wheelrollfric,$wheelspinfric) = (.510, .110, .002); 
# MANY BOTHANS DIED TO BRING US THIS INFORMATION!

my ($wheelstiffness,$wheeldamping) = (30000, 1000);
my ($wmarkx,$wmarky,$wmarkz,$wmarkoff) = (0.01, $wheellen+.002, 0.08, -.0);
my $wmarkkg = 0.0;

my ($wheelx,$wheely,$wheelz) = (-0.05, 0.115, 0.046);
my ($wheelkg) = (.300);

my ($boxsx,$boxsy,$boxsz,$boxkg) = (0.25, 0.16, 0.04, 22/2.2);
my ($boxpx,$boxpy,$boxpz) = (-$wheelx, 0.0, 0.05);
my ($baselateralfric,$baserollfric,$basespinfric) = (.00001, .030, .030);

my ($rwheelrpy) = ("0 $pio2 0");
my ($lwheelrpy) = ("0 -$pio2 0");
my ($scanpx,$scanpy,$scanpz) = (0.022, 0.0, 0.01);
my ($jscanpx,$jscanpy,$jscanpz) = (0.105, 0.0, 0.12);

my ($b2fwheelPos,$fwheelRadius,$fwheelLen,$fwheelKg) =
    ("0.14 0 0.010", .015, 0.005, 0);
my ($fwheelAttachRadius) = (.023);

sub cuboidInertia {
    my ($w,$h,$d,$m) = @_;
    my $ixx = 1.0/12.0*$m*($h*$h+$d*$d);
    my $ixy = 0.0;
    my $ixz = 0.0;
    my $iyy = 1.0/12.0*$m*($w*$w+$h*$h);
    my $iyz = 0.0;
    my $izz = 1.0/12.0*$m*($w*$w+$d*$d);
    return ($ixx,$ixy,$ixz,$iyy,$iyz,$izz);
}
sub cylinderInertia {
    my ($r,$h,$m) = @_;
    my $ixx = 1.0/12.0*$m*(3*$r*$r+$h*$h);
    my $ixy = 0.0;
    my $ixz = 0.0;
    my $iyy = 1.0/12.0*$m*(3*$r*$r+$h*$h);
    my $iyz = 0.0;
    my $izz = 1.0/2.0*$m*$r*$r;
    return ($ixx,$ixy,$ixz,$iyy,$iyz,$izz);
}
sub hollowSphereInertia {
    my ($r,$m) = @_;
    my $ixx = 2.0/3.0*$m*$r*$r;
    my $ixy = 0.0;
    my $ixz = 0.0;
    my $iyy = 2.0/3.0*$m*$r*$r;
    my $iyz = 0.0;
    my $izz = 2.0/3.0*$m*$r*$r;
    return ($ixx,$ixy,$ixz,$iyy,$iyz,$izz);
}
sub inertiaVal {
    my ($ixx,$ixy,$ixz,$iyy,$iyz,$izz) = @_;
    return qq(ixx="$ixx" ixy="$ixy" ixz="$ixz" iyy="$iyy" iyz="$iyz" izz="$izz");
}

my $boxinertia = inertiaVal(cuboidInertia($boxsx,$boxsy,$boxsz,$boxkg));
my $lwheelinertia = inertiaVal(cylinderInertia($lwheelrad,$wheellen,$wheelkg));
my $rwheelinertia = inertiaVal(cylinderInertia($rwheelrad,$wheellen,$wheelkg));
my $fwheelinertia = inertiaVal(cylinderInertia($fwheelRadius,$fwheelLen,$fwheelKg));
my $ballinertia = inertiaVal(hollowSphereInertia(1,1.0));
#printf(STDERR "BALLINERTIA<%s>\n",$ballinertia);

my $wmarkinertia =
    inertiaVal(cuboidInertia($wmarkx,$wmarky,$wmarkz,$wmarkkg));


print <<"EOF";
<robot name="Beevee">

  <link name="base">
    <contact>
      <lateral_friction value="$baselateralfric"/>
      <rolling_friction value="$baserollfric"/>
      <spinning_friction value="$basespinfric"/>
    </contact>
    <inertial>
      <mass value="$boxkg"/>
      <inertia $boxinertia/>
    </inertial>
    <visual>
      <origin rpy="0 0 0" xyz="$boxpx $boxpy $boxpz"/>
      <geometry>
        <box size="$boxsx $boxsy $boxsz"/>
      </geometry>
      <material name="grey888">
        <color rgba=".8 .8 .8 1"/>
      </material>
    </visual>
    <collision>
      <origin rpy="0 0 0" xyz="$boxpx $boxpy $boxpz"/>
      <geometry>
        <box size="$boxsx $boxsy $boxsz"/>
      </geometry>
      <material name="blue">
        <color rgba=".2 .2 1 1"/>
      </material>
    </collision>
  </link>
  
  <link name="lwheel">
    <inertial>
      <mass value="$wheelkg"/>
      <inertia $lwheelinertia/>
    </inertial>
    <contact>
      <lateral_friction value="$wheellateralfric"/>
      <rolling_friction value="$wheelrollfric"/>
      <spinning_friction value="$wheelspinfric"/>
      <stiffness value="$wheelstiffness"/>
      <damping value="$wheeldamping"/>
    </contact>
    <visual>
      <geometry>
        <cylinder length="$wheellen" radius="$lwheelrad"/>
      </geometry>
      <origin rpy="$lwheelrpy" xyz="0 0 0"/>
      <material name="black112">
        <color rgba=".1 .1 .2 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="$wheellen" radius="$lwheelrad"/>
      </geometry>
      <origin rpy="$lwheelrpy" xyz="0 0 0"/>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </collision>
  </link>

  <link name="lwheelmark">
    <inertial>
      <mass value="$wmarkkg"/>
      <inertia $wmarkinertia/>
    </inertial>
    <visual>
      <origin rpy="0 0 0" xyz="0 0 $wmarkoff"/>
      <geometry>
        <box size="$wmarkx $wmarky $wmarkz"/>
      </geometry>
      <material name="blue55a">
        <color rgba=".5 .5 1 1"/>
      </material>
    </visual>
    <collision>
      <origin rpy="0 0 0" xyz="0 0 $wmarkoff"/>
      <geometry>
        <box size="$wmarkx $wmarky $wmarkz"/>
      </geometry>
    </collision>
  </link>

  <joint name="lwheel_lwheelmark" type="fixed">
    <parent link="lwheel"/>
    <child link="lwheelmark"/>
    <origin xyz="0 0 0" rpy="0 0 $pio2"/>
  </joint>

  <joint name="base_lwheel" type="continuous">
    <parent link="base"/>
    <child link="lwheel"/>
    <axis xyz="-1 0 0"/>
    <origin xyz="$wheelx $wheely $wheelz" rpy="0 0 -$pio2"/>
  </joint>
  
  <link name="rwheel">
    <inertial>
      <mass value="$wheelkg"/>
      <inertia $rwheelinertia/>
    </inertial>
    <contact>
      <lateral_friction value="$wheellateralfric"/>
      <rolling_friction value="$wheelrollfric"/>
      <spinning_friction value="$wheelspinfric"/>
    </contact>
    <visual>
      <geometry>
        <cylinder length="$wheellen" radius="$rwheelrad"/>
      </geometry>
      <origin rpy="$rwheelrpy" xyz="0 0 0"/>
      <material name="black131">
        <color rgba=".1 .3 .1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="$wheellen" radius="$rwheelrad"/>
      </geometry>
      <origin rpy="$rwheelrpy" xyz="0 0 0"/>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </collision>
  </link>
  
  <joint name="base_rwheel" type="continuous">
    <parent link="base"/>
    <child link="rwheel"/>
    <axis xyz="1 0 0"/>
    <origin xyz="$wheelx -$wheely $wheelz" rpy="0 0 $pio2"/>
  </joint>
  
  <link name="rwheelmark">
    <inertial>
      <mass value="$wmarkkg"/>
      <inertia $wmarkinertia/>
    </inertial>
    <visual>
      <origin rpy="0 0 0" xyz="0 0 $wmarkoff"/>
      <geometry>
        <box size="$wmarkx $wmarky $wmarkz"/>
      </geometry>
      <material name="green">
        <color rgba="0 1 0 1"/>
      </material>
    </visual>
    <collision>
      <origin rpy="0 0 0" xyz="0 0 $wmarkoff"/>
      <geometry>
        <box size="$wmarkx $wmarky $wmarkz"/>
      </geometry>
    </collision>
  </link>

  <joint name="rwheel_rwheelmark" type="fixed">
    <parent link="rwheel"/>
    <child link="rwheelmark"/>
    <origin xyz="0 0 0" rpy="0 0 -$pio2"/>
  </joint>

  <link name="fattach">
    <visual>
      <geometry>
        <cylinder length="0.060" radius="$fwheelAttachRadius"/>
      </geometry>
      <origin rpy="0 0 0" xyz="0.13 0 0.08"/>
      <material name="white388">
        <color rgba=".3 .8 .8 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.060" radius="$fwheelAttachRadius"/>
      </geometry>
      <origin rpy="0 0 0" xyz="0.13 0 0.08"/>
    </collision>
  </link>
  
  <joint name="base_fattach" type="fixed">
    <parent link="base"/>
    <child link="fattach"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>
  
  <link name="fwheel">
    <inertial>
      <mass value="$fwheelKg"/>
      <inertia $fwheelinertia/>
    </inertial>
    <contact>
      <lateral_friction  value="0.0000001"/>
      <rolling_friction  value="0.0000001"/>
      <spinning_friction value="0.0000001"/>
    </contact>
    <visual>
      <geometry>
        <cylinder length="$fwheelLen" radius="$fwheelRadius"/>
      </geometry>
      <origin rpy="$pio2 0 0" xyz="0 0 0"/>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="$fwheelLen" radius="$fwheelRadius"/>
      </geometry>
      <origin rpy="$pio2 0 0" xyz="0 0 0"/>
    </collision>
  </link>
  
  <joint name="base_fwheel" type="fixed">
    <parent link="base"/>
    <child link="fwheel"/>
    <origin xyz="$b2fwheelPos" rpy="0 0 0"/>
  </joint>
  
 <!--
  <link name="scanner">
    <visual>
      <geometry>
        <box size="0.015 0.045 0.015"/>
      </geometry>
      <origin rpy="0 0 0" xyz="$scanpx $scanpy $scanpz"/>
      <material name="red122">
        <color rgba="1 .2 .2 1"/>
      </material>
    </visual>
  </link>
  
  <joint name="base_scanner" type="fixed">
    <parent link="base"/>
    <child link="scanner"/>
    <origin xyz="$jscanpx $jscanpy $jscanpz" rpy="0 0 0"/>
  </joint>
  -->
</robot>
EOF
    
