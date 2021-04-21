set xsa_path [lindex $argv 0]
set overlay_name [lindex $argv 1]
set board [lindex $argv 2]
set processor [lindex $argv 3]

if { ${processor} eq "psu_cortexa53" } {
	set ps a53
} elseif { ${processor} eq "ps7_cortexa9" } {
	set ps a9
} else {
	puts "Wrong processor name provided."
	exit 1
}

platform -name ${overlay_name} -desc "A vitis platform for ${board}" \
	-hw ${xsa_path} -out ./${board}/output -prebuilt

domain -name xrt -proc ${processor} -os linux \
	-image ./${board}/src/${ps}/xrt/image
domain config -boot ./${board}/src/boot
domain config -bif ./${board}/src/${ps}/xrt/linux.bif
domain -runtime opencl

platform -generate
