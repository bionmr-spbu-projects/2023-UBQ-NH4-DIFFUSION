include common.mk

all: figures/overall_tumbling.png

clean:
	rm -rf data
	rm -rf figures


figures/overall_tumbling.png: ${SCRIPT_DIR}/03_plot_tumbling_correlation_function.py data/fit.csv
	python3 $< \
		--path-to-fit=data/fit.csv \
		--path-to-tumbling-acorr-csv=data/tumbling_acorr_avg.csv \
		--output-directory=figures \

data/fit.csv: ${SCRIPT_DIR}/02_fit_tumbling_correlation_function.py data/tumbling_acorr_avg.csv
	python3 $< \
		--path-to-tumbling-acorr-csv=data/tumbling_acorr_avg.csv \
		--output-directory=data

data/tumbling_acorr_avg.csv: $(strip ${SCRIPT_DIR})/01_calculate_tumbling_correlation_function.py
	python3 "$<" \
	    --path-to-trajectory="$(strip ${TRAJECTORY_PATH})" \
	    --path-to-reference-pdb="$(strip ${REFERENCE_PDB_PATH})" \
	    --path-to-nodes-csv="$(strip ${NODES_PATH})" \
	    --dt-ns="$(strip ${DT_NS})" \
	    --filetype="$(strip ${FILETYPE})" \
	    --pattern="$(strip ${PATTERN})" \
	    --trajectory-length="$(strip ${TRAJECTORY_LENGTH})" \
	    --output-directory=data
