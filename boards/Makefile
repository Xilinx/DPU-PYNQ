BOARD := Ultra96
SUPPORTED = Ultra96 ZCU104 ZCU111

# VITIS_PLATFORM can be:
# 1. downloaded from Xilinx opendownload for specific boards
# 2. built from scratch for specific boards
# 3. provided by users directly, which overrules the previous two
ifeq ($(BOARD),Ultra96)
VITIS_PLATFORM := $(shell pwd)/$(BOARD)/dpu/dpu.xpfm
DOWNLOAD := 0
endif
ifeq ($(BOARD),ZCU104)
VITIS_PLATFORM := $(shell pwd)/$(BOARD)/dpu/dpu.xpfm
DOWNLOAD := 0
endif
ifeq ($(BOARD),ZCU111)
VITIS_PLATFORM := $(shell pwd)/$(BOARD)/dpu/dpu.xpfm
DOWNLOAD := 0
endif

GARBAGE_PATTERNS := *.log *.jou sample_link.ini
GARBAGE_PATTERNS += binary_container_1 packaged_* tmp_*
GARBAGE_PATTERNS += scripts kernel_xml .Xil
GARBAGE := $(foreach DIR,$(SUPPORTED),$(addprefix $(DIR)/,$(GARBAGE_PATTERNS)))

DIR_PRJ = $(shell pwd)/$(BOARD)
DIR_TRD = $(shell pwd)/../vitis-ai-git/DPU-TRD
VIVADO_ROOT := $(XILINX_VIVADO)
RM = rm -f
RMDIR = rm -rf
VIVADO := ${VIVADO_ROOT}/bin/vivado
TARGET := hw

ifeq ($(BOARD),ZCU111)
KERNEL := DPU_SM
else
KERNEL := DPU
endif

.PHONY: all clean check_env
all : check_env dpu.xclbin

check_env :
	@echo "BOARD: ${BOARD}"
	@echo "VITIS_PLATFORM: ${VITIS_PLATFORM}"
	@echo "DOWNLOAD: ${DOWNLOAD}"
	bash check_env.sh

${VITIS_PLATFORM} :
	@echo "Preparing Vitis platform for ${BOARD}..."
	bash get_platform.sh ${BOARD} ${VITIS_PLATFORM} ${DOWNLOAD}

XOCC_OPTS = -t ${TARGET} --platform ${VITIS_PLATFORM} \
	--save-temps --config ${DIR_PRJ}/prj_config \
	--xp param:compiler.userPostSysLinkTcl=${DIR_TRD}/prj/Vitis/syslink/strip_interconnects.tcl

DPU_HDLSRCS=\
	${DIR_PRJ}/kernel_xml/dpu/kernel.xml\
	${DIR_PRJ}/scripts/package_dpu_kernel.tcl\
	${DIR_PRJ}/scripts/gen_dpu_xo.tcl\
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
${DIR_PRJ}/scripts/package_dpu_kernel.tcl: $(DIR_PRJ)/scripts
	cp -f ${DIR_TRD}/prj/Vitis/scripts/package_dpu_kernel.tcl $@
	sed -i 's/set path_to_hdl "..\/..\/dpu_ip"/set path_to_hdl "..\/..\/vitis-ai-git\/DPU-TRD\/dpu_ip"/' $@
${DIR_PRJ}/scripts/package_sfm_kernel.tcl: $(DIR_PRJ)/scripts
	cp -f ${DIR_TRD}/prj/Vitis/scripts/package_sfm_kernel.tcl $@
	sed -i 's/set path_to_hdl "..\/..\/dpu_ip"/set path_to_hdl "..\/..\/vitis-ai-git\/DPU-TRD\/dpu_ip"/' $@

# Kernel name must match kernel name in kernel.xml
DPU_KERN_NAME = DPUCZDX8G
SFM_KERN_NAME = sfm_xrt_top

ifeq ($(KERNEL),DPU_SM)
kernel_xo += binary_container_1/dpu.xo
kernel_xo += binary_container_1/softmax.xo
else
kernel_xo += binary_container_1/dpu.xo
endif

binary_container_1/dpu.xo: $(DPU_HDLSRCS)
	@mkdir -p ${DIR_PRJ}/binary_container_1
	-@$(RM) ${DIR_PRJ}/$@
	cd ${DIR_PRJ} ;\
	$(VIVADO) -mode batch -source scripts/gen_dpu_xo.tcl \
		-tclargs $@ $(DPU_KERN_NAME) ${TARGET} ${BOARD}

binary_container_1/softmax.xo: $(SOFTMAX_HDLSRCS)
	@mkdir -p ${DIR_PRJ}/binary_container_1
	-@$(RM) ${DIR_PRJ}/$@
	cd ${DIR_PRJ} ;\
	$(VIVADO) -mode batch -source scripts/gen_sfm_xo.tcl \
		-tclargs $@ $(SFM_KERN_NAME) ${TARGET} ${BOARD}

dpu.xclbin: $(kernel_xo) $(VITIS_PLATFORM)
	cd ${DIR_PRJ} ;\
	v++ $(XOCC_OPTS) -l --temp_dir binary_container_1 \
		--log_dir binary_container_1/logs \
		--remote_ip_cache binary_container_1/ip_cache -o ${DIR_PRJ}/binary_container_1/$@ $<
	cp -f ${DIR_PRJ}/binary_container_1/link/vivado/vpl/prj/prj.srcs/sources_1/bd/*/hw_handoff/*.hwh \
		${DIR_PRJ}/dpu.hwh
	cp -f ${DIR_PRJ}/binary_container_1/link/vivado/vpl/prj/prj.runs/impl_1/*.bit \
		${DIR_PRJ}/dpu.bit
	cp -f ${DIR_PRJ}/binary_container_1/$@ \
		${DIR_PRJ}/dpu.xclbin

clean:
	$(RMDIR) $(GARBAGE)

cleanall: clean
	$(RMDIR) Ultra96/dpu
	$(RMDIR) ZCU104/zcu104_dpu
	$(RMDIR) ZCU111/dpu
	$(RMDIR) PYNQ-derivative-overlays
