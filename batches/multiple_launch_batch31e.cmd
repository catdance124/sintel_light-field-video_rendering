::This is a batch script for launching multiple Blenders.
::    > .\run_batch.cmd
::    "../clean_files/scenes/05.2_bamboo/05.2b_comp.blend"

@echo off
cd ..
set file_path="../clean_files/scenes/03.1_alley/03.1e_comp.blend"
echo %file_path%
set start_frame=12
set end_frame=61

start python .\run_blender.py %file_path% -resume "4 3" -end "4 4" -fs %start_frame% -fe %end_frame%