::This is a batch script for launching multiple Blenders.
::    > .\run_batch.cmd
::    "../clean_files/scenes/05.2_bamboo/05.2b_comp.blend"

@echo off
cd ..
set file_path="../clean_files/scenes/03.1_alley/03.1g_comp.blend"
echo %file_path%
set start_frame=15
set end_frame=57

start "03.1_alley,03.1g_comp" python .\run_blender.py %file_path% -resume "0 0" -end "8 8" -fs %start_frame% -fe %end_frame%