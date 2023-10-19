include common.mk

all: figure/fit_msd_plot.png

clean:
	rm -rf data
	rm -rf figure

figure/fit_msd_plot.png: $(strip ${SCRIPT_DIR})/04_plot_mean_square_deviation_curve.py data/msd.csv data/fit.csv
	mkdir -p figure/
	python "$<" \
	    --path-to-msd-csv=data/msd.csv \
	    --path-to-fit-csv=data/fit.csv \
	    --output-directory=figure/ \


data/fit.csv: $(strip ${SCRIPT_DIR})/03_fit_mean_square_deviation_curve.py data/msd.csv
	python "$<" \
		--path-to-msd-csv=data/msd.csv \
		--output-directory=data \


data/msd.csv: $(strip ${SCRIPT_DIR})/02_calc_mean_square_deviation_curve.py data/cm.csv
	python3 "$<" \
	    --path-to-cm-csv="data/cm.csv" \
	    --output-directory=data \
	    --msd-length-ns=10 \

data/cm.csv: $(strip ${SCRIPT_DIR})/01_extract_mass_center.py
	python3 "$<" \
	    --path-to-trajectory="$(strip ${TRAJECTORY_PATH})" \
	    --path-to-reference-pdb="$(strip ${REFERENCE_PDB_PATH})" \
	    --dt-ns="$(strip ${DT_NS})" \
	    --filetype="$(strip ${FILETYPE})" \
	    --pattern="$(strip ${PATTERN})" \
	    --trajectory-length="$(strip ${TRAJECTORY_LENGTH})" \
	    --output-directory=data
