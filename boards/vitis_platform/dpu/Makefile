overlay_name := dpu

BOARD=Ultra96
ifeq ($(BOARD),Ultra96)
	device=xczu3eg-sbva484-1-i
endif
ifeq ($(BOARD),ZCU104)
	device=xczu7ev-ffvc1156-2-e
endif
ifeq ($(BOARD),ZCU111)
	device=xczu28dr-ffvg1517-2-e
endif
ifndef device
$(error Please set BOARD to one of the supported boards)
endif

all: block_design bitstream check_timing
	@echo
	@tput setaf 2 ; echo "Built $(overlay_name) successfully!"; tput sgr0;
	@echo

block_design:
	@sed -i "s/\(create_project \)\(.*\)\( -part \)\(.*\)"\
	"/\1$(overlay_name) $(overlay_name)\3$(device)/" \
	$(overlay_name).tcl; \
	sed -i 's/^set design_name \(.*\)/set design_name $(overlay_name)/g' \
	$(overlay_name).tcl; \
	vivado -mode batch -source $(overlay_name).tcl -notrace

bitstream:
	vivado -mode batch -source build_bitstream.tcl -notrace

check_timing:
	vivado -mode batch -source check_timing.tcl -notrace

clean:
	rm -rf $(overlay_name) *.jou *.log NA
