DIR_PRJ = $(shell pwd)/${BOARD}
DIR_TRD = $(shell pwd)/DPUCZDX8G
VIVADO_ROOT := $(XILINX_VIVADO)
RM = rm -f
RMDIR = rm -rf
VIVADO := ${VIVADO_ROOT}/bin/vivado
TARGET := hw
KERNEL := DPU

.PHONY: all clean check_env
all : check_env DPU_TRD dpu.xclbin

# If VITIS_PLATFORM not set by user, will default to expected file output
# of gen_platform.tcl in the board directory
VITIS_PLATFORM ?= ${DIR_PRJ}/platform.xsa

# If platform not provided, generate a platform using the gen_platform.tcl
# script.
${VITIS_PLATFORM}:
	cd ${DIR_PRJ} && \
	vivado -mode batch -source gen_platform.tcl

check_env :
	@echo "BOARD: ${BOARD}"
	@echo "VITIS_PLATFORM: ${VITIS_PLATFORM}"
	bash check_env.sh

# The DPU IP HDL sources for MPSoC live in the DPU TRD flow, hosted on opendownloads
# more info: https://docs.xilinx.com/r/en-US/pg338-dpu/Vitis-DPU-TRD-Flow
DPU_TRD:
	wget -O DPUCZDX8G.tar.gz https://www.xilinx.com/bin/public/openDownload?filename=DPUCZDX8G_VAI_v3.0.tar.gz && \
        tar xf DPUCZDX8G.tar.gz && \
	mv DPUCZDX8G_VAI_v3.0 DPUCZDX8G && \
	rm DPUCZDX8G.tar.gz
	

# Optional parameters from the TRD flow
XOCC_OPTS = -t ${TARGET} --platform ${VITIS_PLATFORM} \
	    --save-temps --config ${DIR_PRJ}/prj_config \
	    --xp param:compiler.userPostSysLinkOverlayTcl=${DIR_TRD}/prj/Vitis/syslink/strip_interconnects.tcl 

DPU_HDLSRCS=\
	${DIR_PRJ}/kernel_xml/dpu/kernel.xml\
	${DIR_PRJ}/scripts/package_dpu_kernel.tcl\
	${DIR_PRJ}/scripts/gen_dpu_xo.tcl\
	${DIR_PRJ}/scripts/bip_proc.tcl\
	${DIR_PRJ}/dpu_conf.vh\
	${DIR_TRD}/dpu_ip/Vitis/dpu/hdl/DPUCZDX8G.v\
	${DIR_TRD}/dpu_ip/Vitis/dpu/inc/arch_def.vh\
	${DIR_TRD}/dpu_ip/Vitis/dpu/xdc/*.xdc\
	${DIR_TRD}/dpu_ip/DPUCZDX8G_*/hdl/DPUCZDX8G_*_dpu.sv\
	${DIR_TRD}/dpu_ip/DPUCZDX8G_*/inc/function.vh\
	${DIR_TRD}/dpu_ip/DPUCZDX8G_*/inc/arch_para.vh

SOFTMAX_HDLSRCS=\
	${DIR_PRJ}/kernel_xml/sfm/kernel.xml\
	${DIR_PRJ}/scripts/package_sfm_kernel.tcl\
	${DIR_PRJ}/scripts/gen_sfm_xo.tcl\
	${DIR_TRD}/dpu_ip/Vitis/sfm/hdl/*.v\
	${DIR_TRD}/dpu_ip/DPUCZDX8G_*/hdl/DPUCZDX8G_*_sfm.sv\
	${DIR_TRD}/dpu_ip/DPUCZDX8G_*/xci/sfm/fp_*/*.xci		

# Rules for copying the necessary scripts for building the DPU design
# Some paths are sed replaced to reflect our boards directory structure
${DIR_PRJ}/kernel_xml/dpu/kernel.xml:
	@mkdir -p $(@D)
	cp -rf ${DIR_TRD}/prj/Vitis/kernel_xml/dpu/kernel.xml $@
${DIR_PRJ}/kernel_xml/sfm/kernel.xml:
	@mkdir -p $(@D)
	cp -rf ${DIR_TRD}/prj/Vitis/kernel_xml/sfm/kernel.xml $@

${DIR_PRJ}/scripts:
	@mkdir -p $@
${DIR_PRJ}/scripts/gen_dpu_xo.tcl: $(DIR_PRJ)/scripts
	cp -f ${DIR_TRD}/prj/Vitis/scripts/gen_dpu_xo.tcl $@
${DIR_PRJ}/scripts/gen_sfm_xo.tcl: $(DIR_PRJ)/scripts
	cp -f ${DIR_TRD}/prj/Vitis/scripts/gen_sfm_xo.tcl $@
${DIR_PRJ}/scripts/bip_proc.tcl : $(DIR_PRJ)/scripts
	cp -f ${DIR_TRD}/prj/Vitis/scripts/bip_proc.tcl $@
${DIR_PRJ}/scripts/package_dpu_kernel.tcl: $(DIR_PRJ)/scripts
	cp -f ${DIR_TRD}/prj/Vitis/scripts/package_dpu_kernel.tcl $@
	sed -i 's/set path_to_hdl "..\/..\/dpu_ip"/set path_to_hdl "..\/DPUCZDX8G\/dpu_ip"/' $@
${DIR_PRJ}/scripts/package_sfm_kernel.tcl: $(DIR_PRJ)/scripts
	cp -f ${DIR_TRD}/prj/Vitis/scripts/package_sfm_kernel.tcl $@
	sed -i 's/set path_to_hdl "..\/..\/dpu_ip"/set path_to_hdl "..\/DPUCZDX8G\/dpu_ip"/' $@

# Kernel name must match kernel name in kernel.xml
DPU_KERN_NAME = DPUCZDX8G
SFM_KERN_NAME = sfm_xrt_top

ifeq ($(KERNEL),DPU_SM)
kernel_xo += binary_container_1/dpu.xo
kernel_xo += binary_container_1/softmax.xo
else
kernel_xo += binary_container_1/dpu.xo
endif

# Added this rule so the sources get happily copied from the extracted TRD
# otherwise makefile will fail
${DPU_HDLSRCS}: ${DPU_TRD}

# Rule to build Vitis DPU kernel
binary_container_1/dpu.xo: ${DPU_HDLSRCS}
	@mkdir -p ${DIR_PRJ}/binary_container_1
	-@$(RM) ${DIR_PRJ}/$@
	cd ${DIR_PRJ} ;\
	$(VIVADO) -mode batch -source scripts/gen_dpu_xo.tcl -notrace -tclargs $@ $(DPU_KERN_NAME) ${TARGET} ${BOARD}

binary_container_1/softmax.xo: $(SOFTMAX_HDLSRCS)
	@mkdir -p ${DIR_PRJ}/binary_container_1
	-@$(RM) ${DIR_PRJ}/$@
	cd ${DIR_PRJ} ;\
	$(VIVADO) -mode batch -source scripts/gen_sfm_xo.tcl \
		-tclargs $@ $(SFM_KERN_NAME) ${TARGET} ${BOARD} 

# Rule to generate the PYNQ overlay binaries, we only use the hardware platform
# software components get taken core of by the PYNQ image, so using the --package.no_image option
dpu.xclbin: $(kernel_xo) $(VITIS_PLATFORM) 
	cd ${DIR_PRJ} ;\
	v++ $(XOCC_OPTS) -l --temp_dir binary_container_1 \
		--log_dir binary_container_1/logs --package.no_image \
		--remote_ip_cache binary_container_1/ip_cache -o ${DIR_PRJ}/binary_container_1/$@ $<
	cp -f ${DIR_PRJ}/binary_container_1/link/vivado/vpl/prj/prj.gen/sources_1/bd/*/hw_handoff/*.hwh \
		${DIR_PRJ}/dpu.hwh
	cp -f ${DIR_PRJ}/binary_container_1/link/vivado/vpl/prj/prj.runs/impl_1/*.bit \
		${DIR_PRJ}/dpu.bit
	cp -f ${DIR_PRJ}/binary_container_1/$@ \
		${DIR_PRJ}/dpu.xclbin

